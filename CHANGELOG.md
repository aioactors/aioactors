# AioActors Changes

## v2.2.1

- Fixed expired timeout for log report in `ActorWithStatistic.wait`

## v2.2.0

- Added `Jitter` structure for progressive timeout calculation

## v2.1.0

- Added `ActorApp.serve` for run default `server` task as Dockerfile default command
- Disabled `Python 3.8` support

## v2.0.0

- Reorganize project strucuture
- Added `ActorApp` class for running multiple `ActorSystems`
- Added `ActorWithStatistic` base class for calc and view processed messages
- Migrated to `poetry` package control
