
import streamlit as st
import pandas as pd
from config.conexion import obtener_conexion


def mostrar_productos():
    st.header("Gestión de productos")

    menu = st.selectbox(
        "Seleccione una operación",
        [
            "Registrar producto",
            "Consultar productos",
            "Editar producto",
            "Eliminar producto"
        ]
    )

    # REGISTRAR PRODUCTO
    if menu == "Registrar producto":
        st.subheader("Registrar nuevo producto")

        with st.form("form_producto"):
            nombre = st.text_input("Nombre del producto")
            descripcion = st.text_area("Descripción")
            precio = st.number_input(
                "Precio",
                min_value=0.01,
                step=0.50
            )
            stock = st.number_input(
                "Stock",
                min_value=0,
                step=1
            )

            guardar = st.form_submit_button(
                "Guardar producto"
            )

        if guardar:
            if nombre.strip() == "":
                st.warning("Ingrese el nombre del producto.")

            else:
                conexion = None
                cursor = None

                try:
                    conexion = obtener_conexion()

                    if conexion is None:
                        return

                    cursor = conexion.cursor()

                    consulta = """
                    INSERT INTO PRODUCTOS
                    (Nombre, Descripcion, Precio, Stock)
                    VALUES (%s, %s, %s, %s)
                    """

                    cursor.execute(
                        consulta,
                        (nombre, descripcion, precio, stock)
                    )

                    conexion.commit()

                    st.success("Producto registrado correctamente.")

                except Exception as error:
                    if conexion is not None:
                        conexion.rollback()

                    st.error(f"Error: {error}")

                finally:
                    if cursor is not None:
                        cursor.close()

                    if conexion is not None and conexion.is_connected():
                        conexion.close()

    # CONSULTAR PRODUCTOS
    elif menu == "Consultar productos":
        st.subheader("Listado de productos")

        conexion = obtener_conexion()

        if conexion is not None:
            cursor = None

            try:
                cursor = conexion.cursor()

                cursor.execute("""
                    SELECT Id_Producto, Nombre,
                           Descripcion, Precio, Stock
                    FROM PRODUCTOS
                    ORDER BY Id_Producto
                """)

                resultados = cursor.fetchall()

                columnas = [
                    "ID",
                    "Nombre",
                    "Descripción",
                    "Precio",
                    "Stock"
                ]

                if resultados:
                    df = pd.DataFrame(
                        resultados,
                        columns=columnas
                    )

                    st.dataframe(
                        df,
                        use_container_width=True,
                        hide_index=True
                    )
                else:
                    st.info("No hay productos registrados.")

            except Exception as error:
                st.error(f"Error al consultar: {error}")

            finally:
                if cursor is not None:
                    cursor.close()

                if conexion.is_connected():
                    conexion.close()

    # EDITAR PRODUCTO
    elif menu == "Editar producto":
        st.subheader("Modificar producto")

        conexion = obtener_conexion()

        if conexion is not None:
            cursor = None

            try:
                cursor = conexion.cursor()

                cursor.execute("""
                    SELECT Id_Producto, Nombre,
                           Descripcion, Precio, Stock
                    FROM PRODUCTOS
                    ORDER BY Id_Producto
                """)

                productos = cursor.fetchall()

            except Exception as error:
                st.error(f"Error: {error}")
                productos = []

            finally:
                if cursor is not None:
                    cursor.close()

                if conexion.is_connected():
                    conexion.close()

            if productos:
                ids = [p[0] for p in productos]

                id_producto = st.selectbox(
                    "Seleccione el producto",
                    ids,
                    format_func=lambda x: next(
                        f"{p[0]} - {p[1]}" for p in productos if p[0] == x
                    )
                )

                producto = next(
                    p for p in productos if p[0] == id_producto
                )

                with st.form("form_editar_producto"):
                    nombre = st.text_input(
                        "Nombre",
                        value=producto[1]
                    )

                    descripcion = st.text_area(
                        "Descripción",
                        value=producto[2] or ""
                    )

                    precio = st.number_input(
                        "Precio",
                        min_value=0.01,
                        value=float(producto[3]),
                        step=0.50
                    )

                    stock = st.number_input(
                        "Stock",
                        min_value=0,
                        value=int(producto[4]),
                        step=1
                    )

                    actualizar = st.form_submit_button(
                        "Actualizar producto"
                    )

                if actualizar:
                    if nombre.strip() == "":
                        st.warning("Ingrese el nombre del producto.")
                    else:
                        conexion = obtener_conexion()

                        if conexion is not None:
                            cursor = None

                            try:
                                cursor = conexion.cursor()

                                cursor.execute("""
                                    UPDATE PRODUCTOS
                                    SET Nombre = %s,
                                        Descripcion = %s,
                                        Precio = %s,
                                        Stock = %s
                                    WHERE Id_Producto = %s
                                """, (
                                    nombre,
                                    descripcion,
                                    precio,
                                    stock,
                                    id_producto
                                ))

                                conexion.commit()

                                st.success("Producto actualizado correctamente.")
                                st.rerun()

                            except Exception as error:
                                conexion.rollback()
                                st.error(f"Error: {error}")

                            finally:
                                if cursor is not None:
                                    cursor.close()

                                if conexion.is_connected():
                                    conexion.close()

            else:
                st.info("No hay productos para modificar.")

    # ELIMINAR PRODUCTO
    elif menu == "Eliminar producto":
        st.subheader("Eliminar producto")

        conexion = obtener_conexion()

        if conexion is not None:
            cursor = None

            try:
                cursor = conexion.cursor()

                cursor.execute("""
                    SELECT Id_Producto, Nombre
                    FROM PRODUCTOS
                    ORDER BY Id_Producto
                """)

                productos = cursor.fetchall()

            except Exception as error:
                st.error(f"Error: {error}")
                productos = []

            finally:
                if cursor is not None:
                    cursor.close()

                if conexion.is_connected():
                    conexion.close()

            if productos:
                opciones = {
                    f"{p[0]} - {p[1]}": p[0]
                    for p in productos
                }

                seleccionado = st.selectbox(
                    "Seleccione el producto que desea eliminar",
                    list(opciones.keys())
                )

                confirmar = st.checkbox(
                    "Confirmo que deseo eliminar este producto"
                )

                if st.button("Eliminar producto"):
                    if confirmar:
                        conexion = obtener_conexion()

                        if conexion is not None:
                            cursor = None

                            try:
                                cursor = conexion.cursor()

                                cursor.execute("""
                                    DELETE FROM PRODUCTOS
                                    WHERE Id_Producto = %s
                                """, (opciones[seleccionado],))

                                conexion.commit()

                                st.success("Producto eliminado correctamente.")
                                st.rerun()

                            except Exception as error:
                                conexion.rollback()
                                st.error(f"Error: {error}")

                            finally:
                                if cursor is not None:
                                    cursor.close()

                                if conexion.is_connected():
                                    conexion.close()
                    else:
                        st.warning("Confirme la eliminación.")

            else:
                st.info("No hay productos para eliminar.")
