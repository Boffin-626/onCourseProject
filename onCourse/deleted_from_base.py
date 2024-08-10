# from line 276

 raise IntegrityError(
                    "The row in table '%s' with primary key '%s' has an "
                    "invalid foreign key: %s.%s contains a value '%s' that "
                    "does not have a corresponding value in %s.%s."
                    % (
                        table_name,
                        primary_key_value,
                        table_name,
                        column_name,
                        bad_value,
                        referenced_table_name,
                        referenced_column_name,
                    )
                )