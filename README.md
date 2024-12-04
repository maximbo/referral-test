# Тестовый проект

- [Документация к API (redoc)](<https://maximbo.pythonanywhere.com/api/redoc/>)
- [Документация к API (swagger)](<https://maximbo.pythonanywhere.com/api/swagger/>)

<h1 id="api-">API для тестового проекта v1.0.0</h1>

## Authentication

* API Key (cookieAuth)
    - Parameter Name: **sessionid**, in: cookie. 

<h1 id="api--coupons">coupons</h1>

## coupons:check-coupon-presence

<a id="opIdcoupons:check-coupon-presence"></a>

`GET /api/coupons/{coupon_code}/check`

Проверка купона на существование и активацию.

<h3 id="coupons:check-coupon-presence-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|coupon_code|path|string|true|none|

> Example responses

> 200 Response

```json
{
  "detail": "string"
}
```

<h3 id="coupons:check-coupon-presence-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](<https://tools.ietf.org/html/rfc7231#section-6.3.1>)|Купон существует и активирован|[Простой ответ с полем detail](<#schemaпростой ответ с полем detail>)|
|404|[Not Found](<https://tools.ietf.org/html/rfc7231#section-6.5.4>)|Купон не найден или не активирован|[Простой ответ с полем detail](<#schemaпростой ответ с полем detail>)|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
cookieAuth
</aside>

## coupons:subscribe-user-to-coupon

<a id="opIdcoupons:subscribe-user-to-coupon"></a>

`POST /api/coupons/{coupon_code}/subscribe`

Присоединиться к другому пользователю через его купон.

<h3 id="coupons:subscribe-user-to-coupon-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|coupon_code|path|string|true|none|

> Example responses

> 201 Response

```json
{
  "detail": "string"
}
```

<h3 id="coupons:subscribe-user-to-coupon-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|201|[Created](<https://tools.ietf.org/html/rfc7231#section-6.3.2>)|Пользователь успешно присоединился|[Простой ответ с полем detail](<#schemaпростой ответ с полем detail>)|
|403|[Forbidden](<https://tools.ietf.org/html/rfc7231#section-6.5.3>)|Ошибка подписки на пользователя|[Простой ответ с полем detail](<#schemaпростой ответ с полем detail>)|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
cookieAuth
</aside>

## coupons:activate-my-coupon

<a id="opIdcoupons:activate-my-coupon"></a>

`POST /api/coupons/mine/activate`

Активировать собственный купон.

> Example responses

> 202 Response

```json
{
  "detail": "string"
}
```

<h3 id="coupons:activate-my-coupon-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|202|[Accepted](<https://tools.ietf.org/html/rfc7231#section-6.3.3>)|Купон успешно активирован|[Простой ответ с полем detail](<#schemaпростой ответ с полем detail>)|
|400|[Bad Request](<https://tools.ietf.org/html/rfc7231#section-6.5.1>)|Купон уже был активирован|[Простой ответ с полем detail](<#schemaпростой ответ с полем detail>)|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
cookieAuth
</aside>

<h1 id="api--users">users</h1>

## users:check-phone-code

<a id="opIdusers:check-phone-code"></a>

`POST /api/users/check-phone-code/`

Проверка кода для авторизации по номеру телефона.

> Body parameter

```json
{
  "phone_number": "string",
  "code": "stri"
}
```

```yaml
phone_number: string
code: stri

```

<h3 id="users:check-phone-code-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|[Входные данные для проверка телефона и кода активации](<#schemaвходные данные для проверка телефона и кода активации>)|true|none|

> Example responses

> 200 Response

```json
{
  "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",
  "phone_number": "string",
  "date_joined": "2019-08-24T14:15:22Z",
  "coupon_code": "string",
  "coupon_code_activated": true
}
```

<h3 id="users:check-phone-code-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](<https://tools.ietf.org/html/rfc7231#section-6.3.1>)|Пользователь авторизован|[Выходные данные после регистрации или входа пользователя](<#schemaвыходные данные после регистрации или входа пользователя>)|
|201|[Created](<https://tools.ietf.org/html/rfc7231#section-6.3.2>)|Пользователь зарегистрирован|[Выходные данные после регистрации или входа пользователя](<#schemaвыходные данные после регистрации или входа пользователя>)|
|400|[Bad Request](<https://tools.ietf.org/html/rfc7231#section-6.5.1>)|Ошибка валидации данных|None|
|401|[Unauthorized](<https://tools.ietf.org/html/rfc7235#section-3.1>)|Неверный телефон или проверочный код|None|

<aside class="success">
This operation does not require authentication
</aside>

## users:login-by-phone

<a id="opIdusers:login-by-phone"></a>

`POST /api/users/login-by-phone/`

Авторизация по номеру телефона.

> Body parameter

```json
{
  "phone_number": "string"
}
```

```yaml
phone_number: string

```

<h3 id="users:login-by-phone-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|[Входные данные для номера телефона](<#schemaвходные данные для номера телефона>)|true|none|

<h3 id="users:login-by-phone-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|201|[Created](<https://tools.ietf.org/html/rfc7231#section-6.3.2>)|Пользователю отправлено сообщение для входа|None|
|400|[Bad Request](<https://tools.ietf.org/html/rfc7231#section-6.5.1>)|Ошибка валидации данных|None|

<aside class="success">
This operation does not require authentication
</aside>

## users:logout

<a id="opIdusers:logout"></a>

`POST /api/users/logout/`

Разлогинить пользователя.

<h3 id="users:logout-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](<https://tools.ietf.org/html/rfc7231#section-6.3.1>)|Пользователь разлогинен|None|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
cookieAuth
</aside>

## users:get-my-profile

<a id="opIdusers:get-my-profile"></a>

`GET /api/users/me/`

Показать пользователю его профиль

> Example responses

> 200 Response

```json
{
  "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",
  "phone_number": "string",
  "date_joined": "2019-08-24T14:15:22Z",
  "coupon_code": "string",
  "coupon_code_activated": true,
  "subscribed_users": {
    "property1": null,
    "property2": null
  }
}
```

<h3 id="users:get-my-profile-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](<https://tools.ietf.org/html/rfc7231#section-6.3.1>)|none|[Выходные данные для профиля пользователя](<#schemaвыходные данные для профиля пользователя>)|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
cookieAuth
</aside>

# Schemas

<h2 id="tocS_Входные данные для номера телефона">Входные данные для номера телефона</h2>
<!-- backwards compatibility -->
<a id="schemaвходные данные для номера телефона"></a>
<a id="schema_Входные данные для номера телефона"></a>
<a id="tocSвходные данные для номера телефона"></a>
<a id="tocsвходные данные для номера телефона"></a>

```json
{
  "phone_number": "string"
}

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|phone_number|string|true|none|none|

<h2 id="tocS_Входные данные для проверка телефона и кода активации">Входные данные для проверка телефона и кода активации</h2>
<!-- backwards compatibility -->
<a id="schemaвходные данные для проверка телефона и кода активации"></a>
<a id="schema_Входные данные для проверка телефона и кода активации"></a>
<a id="tocSвходные данные для проверка телефона и кода активации"></a>
<a id="tocsвходные данные для проверка телефона и кода активации"></a>

```json
{
  "phone_number": "string",
  "code": "stri"
}

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|phone_number|string|true|none|none|
|code|string|true|none|none|

<h2 id="tocS_Выходные данные для профиля пользователя">Выходные данные для профиля пользователя</h2>
<!-- backwards compatibility -->
<a id="schemaвыходные данные для профиля пользователя"></a>
<a id="schema_Выходные данные для профиля пользователя"></a>
<a id="tocSвыходные данные для профиля пользователя"></a>
<a id="tocsвыходные данные для профиля пользователя"></a>

```json
{
  "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",
  "phone_number": "string",
  "date_joined": "2019-08-24T14:15:22Z",
  "coupon_code": "string",
  "coupon_code_activated": true,
  "subscribed_users": {
    "property1": null,
    "property2": null
  }
}

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|id|string(uuid)|true|read-only|none|
|phone_number|string|true|none|none|
|date_joined|string(date-time)|false|none|none|
|coupon_code|string|true|read-only|none|
|coupon_code_activated|boolean|true|read-only|none|
|subscribed_users|object|true|read-only|none|
|» **additionalProperties**|any|false|none|none|

<h2 id="tocS_Выходные данные после регистрации или входа пользователя">Выходные данные после регистрации или входа пользователя</h2>
<!-- backwards compatibility -->
<a id="schemaвыходные данные после регистрации или входа пользователя"></a>
<a id="schema_Выходные данные после регистрации или входа пользователя"></a>
<a id="tocSвыходные данные после регистрации или входа пользователя"></a>
<a id="tocsвыходные данные после регистрации или входа пользователя"></a>

```json
{
  "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",
  "phone_number": "string",
  "date_joined": "2019-08-24T14:15:22Z",
  "coupon_code": "string",
  "coupon_code_activated": true
}

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|id|string(uuid)|true|read-only|none|
|phone_number|string|true|none|none|
|date_joined|string(date-time)|false|none|none|
|coupon_code|string|true|read-only|none|
|coupon_code_activated|boolean|true|read-only|none|

<h2 id="tocS_Простой ответ с полем detail">Простой ответ с полем detail</h2>
<!-- backwards compatibility -->
<a id="schemaпростой ответ с полем detail"></a>
<a id="schema_Простой ответ с полем detail"></a>
<a id="tocSпростой ответ с полем detail"></a>
<a id="tocsпростой ответ с полем detail"></a>

```json
{
  "detail": "string"
}

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|detail|string|true|none|none|
