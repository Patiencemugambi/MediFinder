"""Add medicine_id column to diagnoses table
Revision ID: fb0482aac942
Revises: 9f1579d43c3f
Create Date: 2023-10-05 18:45:32.274101
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite

# revision identifiers, used by Alembic.
revision = 'fb0482aac942'
down_revision = '9f1579d43c3f'
branch_labels = None
depends_on = None

def upgrade():
    # Check if medicine_id column already exists
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    columns = inspector.get_columns('diagnoses')
    column_names = [column['name'] for column in columns]
    
    if 'medicine_id' not in column_names:
        # Add medicine_id column to diagnoses table
        op.add_column('diagnoses', sa.Column('medicine_id', sa.Integer(), nullable=True))
        
        # Create new foreign key constraint
        op.create_foreign_key('fk_diagnoses_medicine_id_medicines', 'diagnoses', 'medicines', ['medicine_id'], ['id'])
        
        # Copy data from hospital_id to medicine_id
        op.execute("UPDATE diagnoses SET medicine_id = hospital_id")
        
        # Drop hospital_id column
        op.drop_column('diagnoses', 'hospital_id')

def downgrade():
    # Add hospital_id column
    op.add_column('diagnoses', sa.Column('hospital_id', sa.Integer(), nullable=False))
    
    # Copy data from medicine_id to hospital_id
    op.execute("UPDATE diagnoses SET hospital_id = medicine_id")
    
    # Create new foreign key constraint
    op.create_foreign_key('fk_diagnoses_hospital_id_hospitals', 'diagnoses', 'hospitals', ['hospital_id'], ['id'])
    
    # Drop medicine_id column
    op.drop_column('diagnoses', 'medicine_id')