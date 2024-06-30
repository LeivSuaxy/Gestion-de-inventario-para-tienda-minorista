-- ID BOSS ON DELETE SET NULL
ALTER TABLE employee
    DROP CONSTRAINT employee_id_boss_94da85ae_fk_employee_ci;
-- Eliminar la constraint del employee Revisar tu caso

-- Le adiciona el mismo CONSTRAINT con el ON DELETE
ALTER TABLE employee
    ADD CONSTRAINT employee_id_boss_94da85ae_fk_employee_ci
        FOREIGN KEY (id_boss) REFERENCES employee (ci) ON DELETE SET NULL DEFERRABLE INITIALLY DEFERRED;

-- ID_INVENTARIO ON DELETE SET NULL TABLE product
ALTER TABLE product
    DROP CONSTRAINT product_id_inventory_54ed25c5_fk_inventory_id_inventory;

ALTER TABLE product
    ADD CONSTRAINT product_id_inventory_54ed25c5_fk_inventory_id_inventory
        FOREIGN KEY (id_inventory) REFERENCES inventory (id_inventory) ON DELETE SET NULL DEFERRABLE INITIALLY DEFERRED;

-- ACCOUNT CI ON DELETE CASCADE
ALTER TABLE account
    DROP CONSTRAINT account_ci_a19b22b2_fk_employee_ci;

ALTER TABLE account
    ADD CONSTRAINT account_ci_a19b22b2_fk_employee_ci
        FOREIGN KEY (ci) REFERENCES employee (ci) ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED;

-- Inventory ON DELETE CASCADE
ALTER TABLE inventory
    DROP CONSTRAINT inventory_id_warehouse_cc99a44d_fk_warehouse_id_warehouse;

ALTER TABLE inventory
    ADD CONSTRAINT inventory_id_warehouse_cc99a44d_fk_warehouse_id_warehouse
        FOREIGN KEY (id_warehouse) REFERENCES warehouse (id_warehouse) ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED;

-- Inventory_Report
ALTER TABLE inventory_report
    DROP CONSTRAINT inventory_report_id_inventory_1d4bb54a_fk_inventory;

ALTER TABLE inventory_report
    ADD CONSTRAINT inventory_report_id_inventory_1d4bb54a_fk_inventory
        FOREIGN KEY (id_inventory) REFERENCES inventory (id_inventory) ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED;

-- Purchase order detail
ALTER TABLE purchase_order_detail
    DROP CONSTRAINT purchase_order_detai_id_inventory_a3205e8f_fk_inventory;

ALTER TABLE purchase_order_detail
    ADD CONSTRAINT purchase_order_detai_id_inventory_a3205e8f_fk_inventory
        FOREIGN KEY (id_inventory) REFERENCES inventory (id_inventory) ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED;

-- 29/6/2024
-- DROP Table
DROP TABLE purchase_order_detail;

-- Alteraciones en las tablas
ALTER TABLE purchase_order
    ADD COLUMN productos_comprados jsonb;

ALTER TABLE sales_report
    ADD COLUMN productos_comprados jsonb;

