from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator, model_validator


class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    category: str
    occasion: str
    color: str
    sizes: list[str]
    price: float
    image_url: str | None
    in_stock: bool

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_product(cls, product):
        return cls(id=product.id, name=product.name, description=product.description, category=product.category,
                   occasion=product.occasion, color=product.color, sizes=[s for s in product.sizes.split(",") if s],
                   price=product.price, image_url=product.image_url, in_stock=product.in_stock)


class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    favorite_colors: list[str] = Field(default_factory=list, max_length=20)
    favorite_categories: list[str] = Field(default_factory=list, max_length=20)
    sizes: list[str] = Field(default_factory=list, max_length=10)
    style_preferences: str = Field(default="", max_length=500)

    @field_validator("name")
    @classmethod
    def name_must_not_be_blank(cls, value):
        value = value.strip()
        if not value:
            raise ValueError("name must not be blank")
        return value


class UserUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    favorite_colors: list[str] | None = Field(default=None, max_length=20)
    favorite_categories: list[str] | None = Field(default=None, max_length=20)
    sizes: list[str] | None = Field(default=None, max_length=10)
    style_preferences: str | None = Field(default=None, max_length=500)

    @field_validator("name")
    @classmethod
    def updated_name_must_not_be_blank(cls, value):
        if value is not None:
            value = value.strip()
            if not value:
                raise ValueError("name must not be blank")
        return value

    @model_validator(mode="after")
    def require_preference_or_name(self):
        if not self.model_fields_set:
            raise ValueError("Provide at least one field to update")
        return self


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    favorite_colors: list[str] = Field(default_factory=list)
    favorite_categories: list[str] = Field(default_factory=list)
    sizes: list[str] = Field(default_factory=list)
    style_preferences: str = ""

    @classmethod
    def from_user(cls, user):
        split = lambda value: [item for item in value.split(",") if item]
        return cls(id=user.id, name=user.name, email=user.email,
                   favorite_colors=split(user.favorite_colors),
                   favorite_categories=split(user.favorite_categories), sizes=split(user.sizes),
                   style_preferences=user.style_preferences)


class ShoppingRequest(BaseModel):
    category: str | None = Field(default=None, max_length=60)
    occasion: str | None = Field(default=None, max_length=60)
    colors: list[str] = Field(default_factory=list, max_length=10)
    size: str | None = Field(default=None, max_length=20)
    min_budget: float | None = Field(default=None, ge=0)
    max_budget: float | None = Field(default=None, gt=0)
    style_preferences: list[str] = Field(default_factory=list, max_length=10)
    limit: int = Field(default=10, ge=1, le=50)

    @model_validator(mode="after")
    def validate_budget_range(self):
        if self.min_budget is not None and self.max_budget is not None and self.min_budget > self.max_budget:
            raise ValueError("min_budget must not exceed max_budget")
        return self


class Recommendation(BaseModel):
    product: ProductResponse
    score: int
    explanation: str


class ShoppingResponse(BaseModel):
    preferences: ShoppingRequest
    recommendations: list[Recommendation]
