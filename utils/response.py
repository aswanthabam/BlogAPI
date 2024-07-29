from rest_framework.response import Response

class CustomResponse:
    @staticmethod
    def get_failure_response(message,data = {}, status_code=400):
        return Response(data={
            'status':'failed',
            'message':message,
            'data':data
        }, status=status_code)
    @staticmethod
    def get_success_response(message, data = {}, status_code=200):
        return Response(data={
            'status':'success',
            'message':message,
            'data':data
        }, status=status_code)