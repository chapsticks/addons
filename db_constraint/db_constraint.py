from dtcloud.fields import Many2one, Many2many
from dtcloud import tools


def m2o_update_db_foreign_key(self, model, column):
    if hasattr(self, 'db_constraint') and self.db_constraint is False:
        sql = """
            SELECT fk.conname, c1.relname, a1.attname, c2.relname, a2.attname, fk.confdeltype
            FROM pg_constraint AS fk
            JOIN pg_class AS c1 ON fk.conrelid = c1.oid
            JOIN pg_class AS c2 ON fk.confrelid = c2.oid
            JOIN pg_attribute AS a1 ON a1.attrelid = c1.oid AND fk.conkey[1] = a1.attnum
            JOIN pg_attribute AS a2 ON a2.attrelid = c2.oid AND fk.confkey[1] = a2.attnum
            WHERE fk.contype = 'f' AND c1.relname=%s and a1.attname = %s
        """
        model._cr.execute(sql, [model._table, self.name])
        existing = {
            (table1, column1): (name, table2, column2, deltype)
            for name, table1, column1, table2, column2, deltype in model._cr.fetchall()
        }
        for k, v in existing.items():
            tools.sql.drop_constraint(model._cr, model._table, v[0])
        return
    return self._update_db_foreign_key(model, column)


def m2m_update_db_foreign_keys(self, model):
    if hasattr(self, 'db_constraint') and self.db_constraint is False:
        sql = """
            SELECT fk.conname, c1.relname, a1.attname, c2.relname, a2.attname, fk.confdeltype
            FROM pg_constraint AS fk
            JOIN pg_class AS c1 ON fk.conrelid = c1.oid
            JOIN pg_class AS c2 ON fk.confrelid = c2.oid
            JOIN pg_attribute AS a1 ON a1.attrelid = c1.oid AND fk.conkey[1] = a1.attnum
            JOIN pg_attribute AS a2 ON a2.attrelid = c2.oid AND fk.confkey[1] = a2.attnum
            WHERE fk.contype = 'f' AND c1.relname=%s and a1.attname in %s
        """
        model._cr.execute(sql, [self.relation, (self.column1, self.column2)])
        existing = {
            (table1, column1): (name, table2, column2, deltype)
            for name, table1, column1, table2, column2, deltype in model._cr.fetchall()
        }
        for k, v in existing.items():
            tools.sql.drop_constraint(model._cr, self.relation, v[0])
        return
    return self._update_db_foreign_keys(model)


setattr(Many2one, '_update_db_foreign_key', getattr(Many2one, 'update_db_foreign_key'))
setattr(Many2one, 'update_db_foreign_key', m2o_update_db_foreign_key)

setattr(Many2many, '_update_db_foreign_keys', getattr(Many2many, 'update_db_foreign_keys'))
setattr(Many2many, 'update_db_foreign_keys', m2m_update_db_foreign_keys)
