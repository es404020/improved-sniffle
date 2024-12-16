from rest_framework import generics,status
from rest_framework.response import Response
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from expenses.models import User, Expense
from expenses.api.serializers import UserSerializer, ExpenseSerializer,CategorySummarySerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from datetime import datetime

class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response_data = serializer.save()
        return Response(
            response_data, 
            status=status.HTTP_201_CREATED
        )

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ExpenseListCreateView(generics.ListCreateAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['user', 'category', 'date']
    search_fields = ['title']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response_data = serializer.save()
        return Response(
            response_data, 
            status=status.HTTP_201_CREATED
        )

class ExpenseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

class ExpenseDateRangeView(generics.ListAPIView):
    serializer_class = ExpenseSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        queryset = Expense.objects.filter(user_id=user_id)
        
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        
        return queryset


class ExpenseCategorySummaryView(generics.ListAPIView):
    serializer_class = CategorySummarySerializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        year = int(self.kwargs.get('year'))
        month = int(self.kwargs.get('month'))

        # Convert year and month to a date range
        start_date = datetime(year, month, 1)
        
        if month == 12:
            end_date = datetime(year + 1, 1, 1)
        else:
            end_date = datetime(year, month + 1, 1)

        category_summary = Expense.objects.filter(
            user_id=user_id,
            date__gte=start_date,
            date__lt=end_date
        ).values('category').annotate(
            total_amount=Sum('amount')
        )

        return category_summary

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)        