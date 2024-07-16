# PyIdentity

PyIdentity is a flexible, high-performance identity and profile management middleware for FastAPI applications. It provides a robust set of tools to handle user authentication, authorization, and profile management, designed to be easily integrated and customized in existing FastAPI projects.

## Features

- Middleware-based integration for seamless FastAPI compatibility
- Customizable routing with plugin architecture
- Core services for JWT claims validation and management
- MongoDB integration with Beanie ODM for efficient data management
- User registration and authentication
- Role-based access control
- Profile management
- Password hashing with Passlib
- Email verification
- Two-factor authentication (2FA)
- GDPR-compliant data handling
- Extensible architecture for custom identity providers

## Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/): Modern, fast web framework for building APIs with Python 3.6+
- [Beanie](https://beanie-odm.dev/): Asynchronous Python object-document mapper (ODM) for MongoDB
- [Pydantic](https://pydantic-docs.helpmanual.io/): Data validation and settings management
- [PyJWT](https://pyjwt.readthedocs.io/): JSON Web Token implementation in Python
- [Passlib](https://passlib.readthedocs.io/): Password hashing library
- [pytest](https://docs.pytest.org/): Testing framework

## Installation

```bash
pip install pyidentity
```

## Quick Start

1. Add PyIdentity middleware to your FastAPI application:

```python
from fastapi import FastAPI
from pyidentity import PyIdentityMiddleware, PyIdentityConfig

app = FastAPI()

identity_config = PyIdentityConfig(
    secret_key="your-secret-key",
    mongodb_url="mongodb://localhost:27017",
    token_expiration=3600
)

app.add_middleware(PyIdentityMiddleware, config=identity_config)
```

2. Use PyIdentity decorators in your routes:

```python
from pyidentity import require_auth, get_current_user

@app.get("/protected")
@require_auth
async def protected_route(current_user = Depends(get_current_user)):
    return {"message": f"Hello, {current_user.username}!"}
```

3. Customize claims validation:

```python
from pyidentity import ClaimsValidator

class CustomClaimsValidator(ClaimsValidator):
    async def validate(self, claims: dict) -> bool:
        # Your custom validation logic here
        return claims.get("role") == "admin"

identity_config.set_claims_validator(CustomClaimsValidator())
```

## Customizing Routes

PyIdentity allows you to easily customize or override default routes:

```python
from pyidentity import PyIdentityRouter

custom_router = PyIdentityRouter()

@custom_router.post("/custom-login")
async def custom_login(credentials: dict):
    # Your custom login logic here
    pass

identity_config.set_router(custom_router)
```

## Core Services

PyIdentity provides core services that you can use in your application:

```python
from pyidentity import get_token_service, get_user_service

@app.get("/user-info")
async def get_user_info(token: str):
    token_service = get_token_service()
    user_service = get_user_service()
    
    claims = await token_service.validate_token(token)
    user = await user_service.get_user_by_id(claims["sub"])
    return user
```

## Documentation

For full documentation, visit [pyidentity.readthedocs.io](https://pyidentity.readthedocs.io).

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for more details.

## License

PyIdentity is released under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Support

If you encounter any problems or have any questions, please [open an issue](https://github.com/onlythompson/pyidentity/issues) on GitHub.

---