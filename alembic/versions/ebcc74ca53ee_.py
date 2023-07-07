"""empty message

Revision ID: ebcc74ca53ee
Revises: 93978ecba2db
Create Date: 2023-07-07 10:02:52.608996

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'ebcc74ca53ee'
down_revision = '93978ecba2db'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('orders_ibfk_6', 'orders', type_='foreignkey')
    op.drop_constraint('orders_ibfk_5', 'orders', type_='foreignkey')
    op.drop_column('orders', 'RefundTransactionId')
    op.drop_column('orders', 'PaymentTransactionId')
    op.add_column('payment_transactions', sa.Column('IsRefund', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('payment_transactions', 'IsRefund')
    op.add_column('orders', sa.Column('PaymentTransactionId', mysql.VARCHAR(length=36), nullable=True))
    op.add_column('orders', sa.Column('RefundTransactionId', mysql.VARCHAR(length=36), nullable=True))
    op.create_foreign_key('orders_ibfk_5', 'orders', 'payment_transactions', ['PaymentTransactionId'], ['id'])
    op.create_foreign_key('orders_ibfk_6', 'orders', 'payment_transactions', ['RefundTransactionId'], ['id'])
    # ### end Alembic commands ###