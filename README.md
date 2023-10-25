# Olympiadnik_v2

## How to build project

- Clone the repository:

``` bash
git clone https://github.com/Minuta18/Olympiadnik_v2.git
cd Olympiadnik_v2
```

- And run code using docker compose:

```bash
docker compose up --build -d
```

## Tables description

### Users

Users table contains all information about user. It can be created with the following command (There and in all code below is PostgreSQL):

```PostgreSQL
CREATE TABLE users (
    id BIGINT NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(15),
    username VARCHAR(255) NOT NULL,
    first_name VARCHAR(63),
    last_name VARCHAR(63),
    middle_name VARCHAR(63),
    is_active SMALLINT NOT NULL,
    is_deleted SMALLINT NOT NULL,
    is_banned SMALLINT NOT NULL,
    permissions SMALLINT NOT NULL,
    password_hashed VARCHAR(255) NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,

    PRIMARY KEY (id),
)
```
