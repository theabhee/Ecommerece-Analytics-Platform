# ESG Emissions Tracker - Database Architecture

## Overview

This document explains how the database architecture for the ESG Emissions Tracker was designed to handle messy real-world enterprise data, perform automatic unit normalization, and maintain a complete audit trail for compliance and verification purposes.

---

## 1. Core Design Principle

The primary rule behind this architecture is:

> **Never modify the raw source data.**

The system stores all incoming values exactly as they are received from source systems. Carbon emissions are calculated separately and stored independently. This ensures data integrity, traceability, and future-proofing if emission factors or reporting standards change.

---

## 2. How the Architecture Meets Key Requirements

### Multi-Tenancy

Every record is associated with a `tenant_id`, ensuring strict data isolation between organizations using the platform.

This allows multiple companies to operate within the same application while maintaining complete separation of their ESG data.

---

### Scope 1, Scope 2, and Scope 3 Tracking

The standard Greenhouse Gas (GHG) Protocol scopes are implemented directly within the backend model.

By enforcing categorization at the database level:

* Scope 1 emissions can be tracked consistently
* Scope 2 emissions can be aggregated easily
* Scope 3 emissions can be analyzed across multiple business activities

This simplifies dashboard generation and reduces frontend complexity.

---

### Unit Normalization Engine

Enterprise sustainability data often arrives in different units such as:

* kWh
* Liters
* Gallons
* Kilometers
* Miles

To address this challenge, the model stores:

* The original value (`raw_value`)
* The original unit (`raw_unit`)
* The emission factor applied
* The standardized carbon output (`computed_co2e`)

This approach ensures that:

* Raw source data remains unchanged
* Emission calculations remain transparent
* Historical records remain valid even if conversion factors change in the future

---

### Source Traceability and Auditing

For compliance and external audits, every record maintains information about:

* Source dataset
* Ingestion timestamp
* Last editor
* Record creation date

This provides a complete audit trail and enables analysts or auditors to verify exactly where each emission figure originated.

---

## 3. Database Schema (Simplified)

```python
class EmissionRecord(models.Model):

    # Multi-Tenant Isolation
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    location = models.CharField(max_length=255)

    # GHG Categorization
    scope = models.CharField(
        choices=[
            ('Scope 1', 'Scope 1'),
            ('Scope 2', 'Scope 2'),
            ('Scope 3', 'Scope 3')
        ]
    )
    category = models.CharField(max_length=255)

    # Normalization Engine
    raw_value = models.FloatField()
    raw_unit = models.CharField(max_length=50)  # e.g. kWh, Liters

    conversion_factor_used = models.FloatField()
    computed_co2e = models.FloatField()  # Standardized output (kg CO2e)

    # Audit Trail
    source_dataset = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_by = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL
    )
```

---

## 4. Datasets Used for Prototype Development

To demonstrate the platform's ability to ingest and normalize fragmented enterprise data, three large datasets were used to simulate common corporate data silos.

### Scope 2 - Electricity Consumption

#### ASHRAE - Great Energy Predictor III

This dataset was used to simulate facility-level electricity usage.

It contains thousands of energy meter readings collected across multiple buildings and sites, making it an excellent representation of utility data typically obtained from facility management systems.

**Purpose:**

* Utility data ingestion
* Electricity normalization
* Scope 2 emissions calculation

---

### Scope 3 - Business Travel

#### Flight Price Prediction Dataset

Business travel is a major contributor to Scope 3 emissions and is often spread across multiple booking platforms.

This dataset was used to simulate travel records and estimate travel-related emissions based on flight routes, durations, and travel activity.

**Purpose:**

* Corporate travel data ingestion
* Scope 3 emissions estimation
* Travel analytics

---

### Scope 1 & Scope 3 - Procurement and Operations

#### SAP Big Query Dataset

Most enterprises rely on SAP-based ERP systems to manage procurement, logistics, and operational data.

This dataset was used to simulate ERP exports and demonstrate the platform's ability to process structured enterprise data at scale.

**Purpose:**

* Procurement data ingestion
* Operational activity tracking
* Supply chain emissions analysis
* Scope 1 and Scope 3 reporting

---

## Conclusion

The architecture was designed around three core principles:

1. **Preserve raw data integrity**
2. **Standardize emissions through a normalization engine**
3. **Maintain a complete audit trail for compliance**

By combining multi-tenant support, automated unit normalization, GHG Protocol categorization, and traceable data lineage, the ESG Emissions Tracker provides a scalable foundation for enterprise sustainability reporting and audit-ready carbon accounting.
