^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changelog for package schunk_svh_tests
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Forthcoming
-----------
* Unify version numbers
  The version convention is as follows:
  `0.1.x` for ROS1 Melodic and Noetic
  `2.0.x` for ROS2 Foxy
  `2.1.x` for ROS2 Humble
  We start with `2.1.0` and bumb that with bloom to `2.1.1` for the first
  release.
* Fix integration test
* Use default hand type for integration tests
  We normally make the distinction on startup via launch file parameters.
  For integration tests, it's sufficient to test with the right hand only.
* Add pipeline for integration testing
  This is a minimal setup that starts the ROS2-control pipeline.
  The driver will currently fail due to a missing serial interface
  (`ttyUSB`) but the output might give insights if the installation
  process is successful on a fresh OS install.
* Contributors: Stefan Scherzinger
