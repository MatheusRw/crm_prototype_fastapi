from sqlalchemy import Integer, String, DateTime, ForeignKey, Numeric, Enum, Text, Boolean, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
import enum

from database import Base


class OpportunityStage(str, enum.Enum):
    new = "new"
    qualified = "qualified"
    proposal = "proposal"
    won = "won"
    lost = "lost"


class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False, index=True)
    email: Mapped[str | None] = mapped_column(String(150), unique=True, nullable=True, index=True)
    phone: Mapped[str | None] = mapped_column(String(50), nullable=True)
    company: Mapped[str | None] = mapped_column(String(150), nullable=True)
    created_at: Mapped["DateTime"] = mapped_column(DateTime(timezone=True), server_default=func.now())

    interactions: Mapped[list["Interaction"]] = relationship(
        "Interaction", back_populates="customer", cascade="all, delete-orphan"
    )
    opportunities: Mapped[list["Opportunity"]] = relationship(
        "Opportunity", back_populates="customer", cascade="all, delete-orphan"
    )


class Interaction(Base):
    __tablename__ = "interactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.id", ondelete="CASCADE"), index=True, nullable=False
    )
    type: Mapped[str] = mapped_column(String(50), nullable=False)  # call, meeting, email, whatsapp, etc.
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    occurred_at: Mapped["DateTime"] = mapped_column(DateTime(timezone=True), server_default=func.now(), index=True)

    customer: Mapped["Customer"] = relationship("Customer", back_populates="interactions")


class Opportunity(Base):
    __tablename__ = "opportunities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.id", ondelete="CASCADE"), index=True, nullable=False
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    stage: Mapped[OpportunityStage] = mapped_column(
        Enum(OpportunityStage, name="opportunity_stage"),
        default=OpportunityStage.new,
        nullable=False,
        index=True,
    )
    value: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True)
    close_date: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), nullable=True)  # Corrigido
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    customer: Mapped["Customer"] = relationship("Customer", back_populates="opportunities")


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(150), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)  # 🔹 usar Boolean explícito
