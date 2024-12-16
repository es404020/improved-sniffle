from rest_framework import serializers
from expenses.models import User, Expense
from decimal import Decimal

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
    def create(self, validated_data):
      
        user = User.objects.create(**validated_data)
        return {'message': f'User successfully created with id {user.id}'}    

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['id', 'user', 'title', 'amount', 'date', 'category']
        read_only_fields = ['id']

    def validate_amount(self, value):
        # Ensure the amount is a positive Decimal
        value = Decimal(str(value))
        if value <= Decimal('0'):
            raise serializers.ValidationError("Amount must be a positive number.")
        return value
    def create(self, validated_data):
        expense = Expense.objects.create(**validated_data)
        return {'message': f'Expense successfully created with id {expense.id}'}

class CategorySummarySerializer(serializers.Serializer):
    category = serializers.CharField()
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2)

