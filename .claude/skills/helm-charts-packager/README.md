# Helm Charts Packager Skill

This skill provides comprehensive support for packaging Kubernetes applications with Helm charts, from basic examples to production-ready charts with proper security and best practices.

## Overview

The Helm Charts Packager skill helps developers create and manage Helm charts for Kubernetes applications. It includes:

- Chart structure and organization best practices
- Template development with Go template syntax and Sprig functions
- Dependency management patterns
- Security considerations and chart signing
- Production-ready chart configurations
- Testing and validation workflows

## Features

- **Smart Chart Generation**: Creates optimized Helm chart structures based on application requirements
- **Template Best Practices**: Implements proper Go template and Sprig function usage
- **Dependency Management**: Handles chart dependencies with proper versioning
- **Security Integration**: Includes chart signing and provenance verification
- **Testing Framework**: Implements Helm test hooks for chart validation
- **Production Patterns**: Ready-to-use configurations for production environments

## Usage

### Automatic Chart Creation

The skill provides guidance for creating charts from scratch:

1. Use `helm create <chart-name>` to generate basic structure
2. Customize templates and values based on application needs
3. Add dependencies as required
4. Test and validate the chart before deployment

### Manual Configuration

Review the reference documentation for detailed patterns and best practices:
- Chart structure (`references/chart-structure.md`)
- Templates and values (`references/templates-values.md`)
- Dependencies management (`references/dependencies.md`)
- Security and signing (`references/security.md`)

## Components

- `SKILL.md`: Main skill documentation and usage instructions
- `references/`: Detailed documentation on Helm best practices
- `.yaml` templates: Sample configurations for various chart types

## Best Practices Implemented

- Proper chart structure with Chart.yaml, values.yaml, templates/
- Template helper functions for consistent naming and labeling
- Conditional resource creation based on values
- Dependency management with proper versioning
- Chart testing with test hooks
- Security practices with chart signing
- RBAC separation for security
- Resource requests and limits in templates

## Production Considerations

When creating production charts, consider:
- Implementing proper testing with test hooks
- Using chart signing for integrity verification
- Following semantic versioning for chart releases
- Separating RBAC and ServiceAccount configurations
- Validating user inputs in templates
- Using conditional logic for optional features
- Proper resource management with requests and limits