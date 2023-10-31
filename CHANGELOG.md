# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.0.2] - 2023-10-31
### Added

* .env
* cookies_snapshot

### Modified

* auto_changelog.ipynb
	+ Added imports for `os` and `dotenv`
	+ Replaced hardcoded email and password with environment variables `EMAIL` and `PASSW`
	+ Saved cookies to the local directory instead of logging them to the console
* .gitignore
	+ Ignored the `.env` and `cookies_snapshot` directories

## [0.0.1] - 2023-10-31
### Added
- Initial release
- Add a changelog
- Add a readme
- Add a license
- Add a jupyter notebook with code to generate a changelog
