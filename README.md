## Проект YaMDb собирает отзывы пользователей на произведения.

### Описание.
Проект YaMDb - командная работа.

Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка». Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Жуки» и вторая сюита Баха. Список категорий может быть расширен (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»).

Произведению может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»).

Добавлять произведения, категории и жанры может только администратор.
Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число).

Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи.
На одно произведение пользователь может оставить только один отзыв.

### Стек.

Python==3.7

requests==2.26.0

django==2.2.16

djangorestframework==3.12.4

PyJWT==2.1.0

pytest==6.2.4

djangorestframework-simplejwt==5.2.0

### Примеры использования API.

Получение произведений:
``` 
GET /api/v1/titles/
``` 
Добавление произведения (только администратор):
``` 
POST /api/v1/titles/
```
В параметрах передавать json
``` 
{
    "name": "Название произведения",
    "year": 1990,
    "description": "Описание произведения",
    "genre": [
    "fantasy"
    ],
    "category": "films"
}
``` 

