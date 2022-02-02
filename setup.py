def setup_tables(cursor):

    # Create the database
    cursor.execute("CREATE DATABASE IF NOT EXISTS banana_cyber_cafe;")
    cursor.execute("USE banana_cyber_cafe;")

    COMPUTERS_TABLE = """
    CREATE TABLE IF NOT EXISTS computers(
        id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        ip_address VARCHAR(255) NOT NULL UNIQUE,
        status VARCHAR(255) NOT NULL
    );
    """

    SOFTWARES_TABLE = """
    CREATE TABLE IF NOT EXISTS software_installed(
        name VARCHAR(255) NOT NULL,
        version VARCHAR(255) NOT NULL,
        computer_id INT NOT NULL,
        PRIMARY KEY(name, computer_id),
        FOREIGN KEY(computer_id) REFERENCES computers(id)
    )
    
    """

    cursor.execute(COMPUTERS_TABLE)
    cursor.execute(SOFTWARES_TABLE)