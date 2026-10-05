# Cómo instalar la firma de Oryzz

Tiempo: 5 minutos por persona. Hay dos firmas por persona:

| Firma | Cuándo | Lleva imagen |
|---|---|---|
| **Completa** | Correos nuevos | Sí (avatar de 56 px) |
| **Compacta** | Respuestas y reenvíos | No |

Archivos: `firma_juan-salazar_completa.html`, `firma_juan-salazar_compacta.html`, `firma_david-morales_*`, `firma_oryzz-tap_*` (+ su versión `.txt`).

---

## 0. Antes de nada (una sola vez)

1. **Sube las imágenes.** Copia el contenido de `08_Email/assets/` a `https://oryzz.com/brand/email/` (o a otra URL pública). La firma solo usa `firma-avatar-oryzz.png` y `firma-avatar-tap.png`, pero conviene subirlo todo: las plantillas usan el resto.
   Comprueba que abre en el navegador: `https://oryzz.com/brand/email/firma-avatar-oryzz.png`.
2. **Si usas otra URL**, cámbiala en `_copiar_firmas.html` (constante `BASE_URL`, al principio del archivo) y, si vas a usar los `.html` sueltos, busca y reemplaza `https://oryzz.com/brand/email` en ellos.
3. **Pon tus datos.** En `_copiar_firmas.html`, edita el bloque `DATOS` del principio (correo y teléfono de cada uno). Los `.html` sueltos llevan `{{email_juan}}`, `{{telefono_juan}}`…: reemplázalos a mano.

> Si al abrir `_copiar_firmas.html` sale un aviso naranja de «Las imágenes no están subidas todavía», no copies la firma completa: Gmail la guardaría sin logo. La compacta sí se puede instalar ya.

---

## 1. Gmail (web)

1. Abre `firmas/_copiar_firmas.html` en Chrome (doble clic).
2. Pulsa **Copiar firma** en la *completa* de tu nombre.
3. En Gmail: icono del engranaje → **Configuración → Ver todos los ajustes → General → Firma → + Crear**. Nombre: `Oryzz completa`.
4. Pega (Ctrl+V / Cmd+V) en el cuadro de la firma. No cambies la fuente desde el editor de Gmail.
5. Repite con la *compacta* (nombre: `Oryzz compacta`).
6. En **Valores predeterminados de firma**:
   - *Para correos nuevos:* `Oryzz completa`
   - *Al responder o reenviar:* `Oryzz compacta`
7. Marca **«Insertar esta firma antes del texto citado en las respuestas…»**.
8. Baja del todo y pulsa **Guardar cambios**.

Comprueba: redacta un correo nuevo a ti mismo y ábrelo en el móvil.

**Si pegar no conserva el diseño:** abre el `.html` suelto de la firma en Chrome, selecciona todo (Ctrl+A), copia y pega. No copies desde el código fuente.

### Gmail en el móvil (app)

La app solo admite firma de texto y solo la usa si no hay firma web. Ajustes → tu cuenta → **Firma para móvil** → pega el contenido del `.txt` compacto, p. ej.:

```
Juan Salazar · Oryzz
Estrategia & Ads · +34 600 000 000 · oryzz.com
```

## 2. Outlook

**Outlook web y el nuevo Outlook (Windows/Mac):** Configuración → Cuentas → **Firmas** → Nueva firma → pega desde `_copiar_firmas.html` → en «Seleccionar firmas predeterminadas», completa para mensajes nuevos y compacta para respuestas → Guardar.

**Outlook clásico de escritorio (Windows):**
- Opción rápida: Archivo → Opciones → Correo → **Firmas…** → Nueva → pega → elige las predeterminadas.
- Opción exacta: cierra Outlook, copia `firma_<nombre>_completa.html` en `%APPDATA%\Microsoft\Signatures\` renombrado a `Oryzz completa.htm` (ya con tus datos reales) y vuelve a abrir Outlook. Aparecerá en la lista de firmas.

Outlook de escritorio no aplica el redondeo del avatar (se verá cuadrado). Es normal.

## 3. Apple Mail (Mac)

Mail → Ajustes → **Firmas** → + → pega la firma → **desmarca** «Usar siempre mi tipo de letra predeterminado del mensaje». Apple Mail no permite una firma distinta para respuestas: usa la completa.

---

## Reglas

- No añadas frases motivacionales, banners, iconos de redes de colores ni avisos legales de cinco líneas.
- Nada de fotos personales en la firma completa: el avatar de marca es igual para todos (coherencia y menos peso).
- Si cambia un dato (teléfono, rol), cámbialo en `00_Fuente_Maestra/build/email_build.py` (diccionario `FIRMAS`) y vuelve a ejecutar `python email_build.py plantillas`, o edita los `.html` a mano.
- El texto de la firma usa Arial a propósito: Gmail y Outlook no cargan fuentes web en las firmas.
