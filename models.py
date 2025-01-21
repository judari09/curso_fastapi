from pydantic import BaseModel
from sqlalchemy import ForeignKey
from sqlmodel import Relationship, SQLModel, Field

class CustomerPlan(SQLModel, table=True):
    """
    Modelo que representa la relación muchos a muchos entre clientes y planes.

    Atributos:
        id (int): Identificador único de la relación.
        plan_id (int): Identificador del plan relacionado.
        customer_id (int): Identificador del cliente relacionado.
    """
    id: int = Field(primary_key=True)
    plan_id: int = Field(foreign_key="plan.id")
    customer_id: int = Field(foreign_key="customer.id")

class PlanBase(SQLModel):
    """
    Modelo que representa un plan ofrecido a los clientes.

    Atributos:
        name (str): Nombre del plan.
        price (int): Precio del plan.
        description (str): Descripción del plan.
    """
    name: str = Field(default=None)
    price: int = Field(default=None)
    description: str = Field(default=None)

class PlanCreate(PlanBase):
    pass

class Plan(PlanBase,table=True):
    id: int | None = Field(default=None, primary_key=True)
    customers: list['Customer'] = Relationship(back_populates="plans", link_model=CustomerPlan)

class CustomerBase(SQLModel):
    """
    Clase base para representar información básica de un cliente.

    Atributos:
        name (str): Nombre del cliente.
        description (str | None): Descripción del cliente.
        email (str): Correo electrónico del cliente.
        age (int): Edad del cliente.
    """
    name: str = Field(default=None)
    description: str | None = Field(default=None)
    email: str = Field(default=None)
    age: int = Field(default=None)

class CustomerCreate(CustomerBase):
    """
    Clase para crear un cliente heredando de CustomerBase.
    """
    pass

class Customer(CustomerBase, table=True):
    """
    Modelo que representa a un cliente.

    Atributos:
        id (int | None): Identificador único del cliente.
        transactions (list[Transaction]): Lista de transacciones asociadas al cliente.
        plans (list[Plan]): Lista de planes asociados al cliente.
    """
    id: int | None = Field(default=None, primary_key=True)
    transactions: list["Transaction"] = Relationship(back_populates="customer")
    plans: list[Plan] = Relationship(back_populates="customers", link_model=CustomerPlan)

class TransactionBase(SQLModel):
    """
    Clase base para representar información básica de una transacción.

    Atributos:
        ammount (int): Monto de la transacción.
        description (str): Descripción de la transacción.
    """
    ammount: int = Field(default=None)
    description: str = Field(default=None)

class TransactionCreate(TransactionBase):
    """
    Clase para crear una transacción heredando de TransactionBase.

    Atributos:
        customer_id (int): Identificador del cliente asociado a la transacción.
    """
    customer_id: int = Field(foreign_key="customer.id")

class Transaction(TransactionBase, table=True):
    """
    Modelo que representa una transacción.

    Atributos:
        id (int | None): Identificador único de la transacción.
        customer_id (int): Identificador del cliente asociado a la transacción.
        customer (Customer): Cliente asociado a la transacción.
    """
    id: int | None = Field(default=None, primary_key=True)
    customer_id: int = Field(foreign_key="customer.id")
    customer: Customer = Relationship(back_populates="transactions")

class Invoice(BaseModel):
    """
    Modelo que representa una factura.

    Atributos:
        id (int): Identificador único de la factura.
        customer (Customer): Cliente al que pertenece la factura.
        transaction (list[Transaction]): Lista de transacciones incluidas en la factura.
        total (int): Total acumulado de la factura.
    """
    id: int 
    customer: Customer
    transaction: list[Transaction]
    total: int

    @property
    def ammount_total(self):
        """
        Calcula el monto total de todas las transacciones en la factura.

        Retorna:
            int: Suma del monto de todas las transacciones.
        """
        return sum(transaction.ammount for transaction in self.transaction)
