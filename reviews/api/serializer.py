from rest_framework import serializers

from reviews.models import Book, Publisher, BookContributor, Contributor


class BookSerailizer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class PublisherSerailizer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = '__all__'


class BookContributorSerailizer(serializers.ModelSerializer):
    book = BookSerailizer()
    class Meta:
        model = BookContributor
        fields = ['book', 'role']


class ContributorSerializer(serializers.ModelSerializer):
    bookcontributor_set = BookContributorSerailizer(read_only=True, many=True)
    number_contributions = serializers.ReadOnlyField()
    class Meta:
        model = Contributor
        fields = ['first_names', 'last_names', 'email', 'number_contributions', 'bookcontributor_set']