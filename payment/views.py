from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from sslcommerz_lib import SSLCOMMERZ
from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth.models import User
# from orders.models import Order
import uuid
import json
import requests
from django.views.decorators.csrf import csrf_exempt
import logging
logger = logging.getLogger(__name__)
from rest_framework import viewsets

class PaymentViewSet(viewsets.ViewSet):
    # queryset = Payment.objects.all()
    # serializer_class = PaymentSerializer

    # @action(detail=False, methods=['post'])
    # def create_payment(self, request):
    def create(self, request):
        # print("rabiul")
        logger.info(f"Received data: {request.data}")
        store_id = 'phitr67b2aebc616ac'
        store_pass = 'phitr67b2aebc616ac@ssl'

        trx_id = str(uuid.uuid4())[:10].replace('-', '').upper()
        user_id = request.data.get('user')
        amount = request.data.get('amount') 
        orderIds = request.data.get('orderIds') 
        
        # print(amount)
         
        settings = {'store_id': store_id,
                    'store_pass': store_pass, 'issandbox': True}
        
        
        sslcommez = SSLCOMMERZ(settings)
        print(sslcommez)
        post_body = {}
        post_body['total_amount'] = amount
        post_body['currency'] = "BDT"
        post_body['tran_id'] = trx_id
        # post_body['success_url'] = f'https://github.com/rabi993'
        post_body['success_url'] = request.build_absolute_uri(f'success/?trx_id={trx_id}&user_id={user_id}&orderIds={orderIds}&amount={amount}')
        # post_body['success_url'] = f'http://127.0.0.1:5501/MyDonateHistory.html'
        post_body['fail_url'] = request.build_absolute_uri(f'fail/?trx_id={trx_id}&user_id={user_id}&orderIds={orderIds}&amount={amount}')

        post_body['cancel_url'] = request.build_absolute_uri(f'cancle/?trx_id={trx_id}&user_id={user_id}&orderIds={orderIds}&amount={amount}')
        post_body['emi_option'] = 0
        post_body['cus_email'] = "test@test.com"
        post_body['cus_phone'] = "01700000000"
        post_body['cus_add1'] = 'Dhaka' 
        post_body['cus_city'] = 'Uttara'
        post_body['cus_country'] = 'Bangladesh'
        post_body['shipping_method'] = "NO"
        post_body['multi_card_name'] = ""
        post_body['num_of_item'] = 1
        post_body['product_name'] = "Test"
        post_body['product_category'] = "Test Category"
        post_body['product_profile'] = "general"


        response = sslcommez.createSession(post_body)
        print(response)

        return Response(response['GatewayPageURL'])
    @csrf_exempt
    @action(detail=False, methods=['post'])
    def success(self, request):
        try:
            user_id = request.query_params.get('user_id')
            trx_id = request.query_params.get('trx_id')
            orderIds = request.query_params.get('orderIds', '[]')
            amount = request.query_params.get('amount')

            orderIds = json.loads(orderIds)  # Convert from string to list
            logger.info(f"Received transaction details: {request.query_params}")

            if not user_id:
                return Response({"error": "User ID is required"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)

            for order_id in orderIds:
                url = f"https://flowers-world-two.vercel.app/orders/{order_id}/"
                response = requests.patch(url, json={"paid": True}, headers={"Content-Type": "application/json"})

            return redirect('https://rabi993.github.io/flowers-world-frontend-with-OnrenderAPI/myOrders.html')

        except Exception as e:
            logger.error(f"Error: {str(e)}")
            return Response({"error": "Internal Server Error", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

        
    @action(detail=False, methods=['post'])
    def fail(self, request):
        return self._handle_fail_payment(request, "cancel")

    @action(detail=False, methods=['post'])
    def cancel(self, request):
        return self._handle_cancel_payment(request, "cancel")

    
    def _handle_cancel_payment(self, request, action_type):
        try:
            user_id = request.query_params.get('user_id')
            orderIds = request.query_params.get('orderIds', '[]')

            orderIds = json.loads(orderIds)  # Convert from string to list
            logger.info(f"Received transaction details ({action_type}): {request.query_params}")

            if not user_id:
                return Response({"error": "User ID is required"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)

            # Perform DELETE request for each order ID
            for order_id in orderIds:
                url = f"https://flowers-world-two.vercel.app/orders/{order_id}/"
                response = requests.delete(url)

                if response.status_code != 204:  # 204 No Content is expected for DELETE
                    logger.error(f"Failed to delete order {order_id}: {response.status_code} - {response.text}")

            return redirect('https://rabi993.github.io/flowers-world-frontend-with-OnrenderAPI/allflowers.html')

        except Exception as e:
            logger.error(f"Error ({action_type}): {str(e)}")
            return Response({"error": "Internal Server Error", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def _handle_fail_payment(self, request, action_type):
        try:
            user_id = request.query_params.get('user_id')
            orderIds = request.query_params.get('orderIds', '[]')

            orderIds = json.loads(orderIds)  # Convert from string to list
            logger.info(f"Received transaction details ({action_type}): {request.query_params}")

            if not user_id:
                return Response({"error": "User ID is required"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)

            # Perform DELETE request for each order ID
            for order_id in orderIds:
                url = f"https://flowers-world-two.vercel.app/orders/{order_id}/"
                response = requests.delete(url)

                if response.status_code != 204:  # 204 No Content is expected for DELETE
                    logger.error(f"Failed to delete order {order_id}: {response.status_code} - {response.text}")

            return redirect('https://rabi993.github.io/flowers-world-frontend-with-OnrenderAPI/allflowers.html')

        except Exception as e:
            logger.error(f"Error ({action_type}): {str(e)}")
            return Response({"error": "Internal Server Error", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
