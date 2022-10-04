# импортируем filterset, чем-то напоминающий знакомые дженерики
from django_filters import FilterSet, DateTimeFromToRangeFilter
from django_filters.widgets import DateRangeWidget, RangeWidget
from .models import Post


# создаём фильтр
class PostFilter(FilterSet):
    heading_post = CharFilter(field_name='heading', lookup_expr='icontains', label='Заголовок')
    author_post = CharFilter(field_name='author__user__username', lookup_expr='icontains', label='Имя пользователя(Автор)')
    create_time_post = DateFilter(field_name='create_time', lookup_expr='gte', label='Дата(yyyy-mm-dd)')


    # Здесь в мета классе надо предоставить модель и указать поля, по которым будет фильтроваться (т. е. подбираться) информация о товарах

    class Meta:
        model = Post
        # поля, которые мы будем фильтровать (т. е. отбирать по каким-то критериям, имена берутся из моделей)
        fields = {'author', 'dateCreation', 'categoryType'}
