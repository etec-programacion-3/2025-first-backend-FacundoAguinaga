TORTOISE_ORM = {
    "connections": {"default": "sqlite://biblioteca.db"},
    "apps": {
        "models": {
            "models": ["app.models"],
            "default_connection": "default",
        }
    },
}