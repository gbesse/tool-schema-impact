# tool-schema-impact

## Français

Produire des témoins de compatibilité entre schémas JSON restreints.

Données fictives ; aucun accès réseau ni secret requis.

```sh
python -m tool_schema_impact examples/demo.json --lang fr
python -m unittest discover -s tests -v
```

### Méthode et différence

Construit des arguments acceptés par l’ancien schéma mais refusés par le nouveau, en combinant valeurs d’énumération et frontières de types, tailles et nombres. Les mots-clés hors sous-ensemble sont refusés au lieu d’être ignorés.

### Limites

Objets plats fermés, huit propriétés et 100 000 combinaisons maximum. L’absence de témoin dans cette base finie n’est pas une preuve générale d’inclusion JSON Schema ou de compatibilité MCP.

### Validation

Tests de domaine, cas limites et interface FR/EN/ES. La CI teste Python 3.11/3.13 et exécute la wheel installée hors du checkout. JSON conserve les identifiants techniques et les données fournis. Erreur d’entrée : code de sortie 2.

## English

Produce compatibility witnesses between restricted JSON schemas.

Synthetic data; no network access or secret required.

```sh
python -m tool_schema_impact examples/demo.json --lang en
python -m unittest discover -s tests -v
```

### Method and difference

Constructs arguments accepted by the old schema but rejected by the new, combining enum values and type/length/numeric boundaries. Keywords outside the supported subset are rejected rather than ignored.

### Limits

Flat closed objects, at most eight properties and 100,000 combinations. No witness in this finite basis is not a general JSON Schema inclusion or MCP compatibility proof.

### Validation

Domain tests, boundary cases and FR/EN/ES interface. CI tests Python 3.11/3.13 and runs the installed wheel outside the checkout. JSON preserves technical identifiers and supplied data. Invalid input exits with code 2.

## Español

Producir testigos de compatibilidad entre esquemas JSON restringidos.

Datos sintéticos; no requiere red ni secretos.

```sh
python -m tool_schema_impact examples/demo.json --lang es
python -m unittest discover -s tests -v
```

### Método y diferencia

Construye argumentos aceptados por el esquema antiguo y rechazados por el nuevo, combinando enumeraciones y fronteras de tipos, longitudes y números. Rechaza palabras clave no admitidas en lugar de ignorarlas.

### Límites

Objetos planos cerrados, máximo ocho propiedades y 100.000 combinaciones. Ausencia de testigo en esta base finita no prueba inclusión general de JSON Schema ni compatibilidad MCP.

### Validación

Pruebas de dominio, casos límite e interfaz FR/EN/ES. CI prueba Python 3.11/3.13 y ejecuta la wheel instalada fuera del repositorio. JSON conserva identificadores técnicos y datos proporcionados. Entrada inválida termina con código 2.

## Sources / Fuentes

- https://json-schema.org/understanding-json-schema/reference/object
- https://modelcontextprotocol.io/specification/draft/server/tools
