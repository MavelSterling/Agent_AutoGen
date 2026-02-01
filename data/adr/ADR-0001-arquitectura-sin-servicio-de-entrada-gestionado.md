# ADR-0001 - Arquitectura sin servicio de entrada gestionado

## Contexto
El alcance prohibe componentes de entrada API gestionados.

## Opciones
- Servicio gestionado de entrada API
- Control en runtime
- Reverse proxy

## Decision
Usar controles en la capa de aplicacion y red.

## Consecuencias
- La API implementa autenticacion, autorizacion y rate limit.
- Se debe observar trafico directamente en runtime.
