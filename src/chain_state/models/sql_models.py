from decimal import Decimal
from typing import Optional, cast

from sqlalchemy.orm import declarative_base, Mapped
from sqlalchemy import Column, BigInteger, String, ForeignKey

Base = declarative_base()


class ContractCall(Base):
    __tablename__ = "contract_calls"

    id: Mapped[int] = Column(BigInteger, primary_key=True)
    interface_address: Mapped[str] = Column(String(40), required=True)
    implementation_address: Mapped[str] = Column(String(40), required=True)
    function_name: Mapped[str] = Column(String(255), required=True)
    # TODO: num args - verify with ABI
    # TODO: num outputs - verify with ABI


class ContractCallArg(Base):
    __tablename__ = "contract_call_args"

    id: Mapped[int] = Column(BigInteger, primary_key=True)
    contract_call_id: Mapped[int] = Column(BigInteger, ForeignKey(ContractCall.id))
    type: Mapped[str] = Column(String(255))  # TODO: enum

