openapi: 3.1.0
info:
  title: AutoFix.AI Platform API
  version: 1.0.0
  description: >
    Full automated mobile mechanic system using OBD-II dongles, AI diagnostics,
    auto-scheduling, parts ordering, mechanic routing, customer billing, 
    and nationwide scaling.

servers:
  - url: https://api.autofix.ai
    description: Production server
  - url: https://sandbox.autofix.ai
    description: Sandbox

paths:

  ###########################################################################
  # VEHICLES
  ###########################################################################

  /vehicles:
    post:
      summary: Register a vehicle to a user
      tags: [Vehicles]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/VehicleCreate'
      responses:
        '201':
          description: Vehicle registered
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Vehicle'

  /vehicles/{vehicleId}:
    get:
      summary: Get vehicle details
      tags: [Vehicles]
      parameters:
        - $ref: '#/components/parameters/VehicleId'
      responses:
        '200':
          description: Vehicle info
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Vehicle'

  ###########################################################################
  # DONGLE DATA INGESTION
  ###########################################################################

  /dongle/diagnostic:
    post:
      summary: Receive diagnostic event from OBD-II dongle
      tags: [Diagnostics]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/DiagnosticEvent'
      responses:
        '200':
          description: Event processed

  ###########################################################################
  # AI DIAGNOSTICS ENGINE
  ###########################################################################

  /ai/diagnose:
    post:
      summary: AI determines needed repair + parts + severity
      tags: [AI]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/AIDiagnosisRequest'
      responses:
        '200':
          description: AI diagnosis result
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AIDiagnosis'

  ###########################################################################
  # PARTS AUTOMATION
  ###########################################################################

  /parts/order:
    post:
      summary: Auto-order parts for an upcoming job
      tags: [Parts]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PartsOrderRequest'
      responses:
        '200':
          description: Parts ordered
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PartsOrder'

  ###########################################################################
  # SCHEDULING ENGINE
  ###########################################################################

  /appointments/auto:
    post:
      summary: Auto-generate appointment times for a customer
      tags: [Scheduling]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/AutoScheduleRequest'
      responses:
        '200':
          description: Slots generated
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AutoScheduleOptions'

  /appointments/{apptId}/confirm:
    post:
      summary: Customer confirms appointment slot
      tags: [Scheduling]
      parameters:
        - $ref: '#/components/parameters/ApptId'
      responses:
        '200':
          description: Appointment confirmed
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Appointment'

  ###########################################################################
  # MECHANIC OPERATIONS
  ###########################################################################

  /mechanic/jobs:
    get:
      summary: List upcoming mechanic jobs
      tags: [Mechanics]
      responses:
        '200':
          description: Jobs
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Job'

  /mechanic/job/{jobId}/complete:
    post:
      summary: Mechanic marks job finished → triggers billing
      tags: [Mechanics]
      parameters:
        - $ref: '#/components/parameters/JobId'
      responses:
        '200':
          description: Job completed + payment triggered

  ###########################################################################
  # PAYMENTS
  ###########################################################################

  /payments/charge:
    post:
      summary: Charge customer after job completion
      tags: [Payments]
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ChargeRequest'
      responses:
        '200':
          description: Charge successful
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ChargeResult'

  ###########################################################################
  # ADMIN DASHBOARD (Phase 3)
  ###########################################################################

  /admin/vehicles:
    get:
      summary: List all vehicles in system
      tags: [Admin]
      responses:
        '200':
          description: List
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Vehicle'

  /admin/events:
    get:
      summary: All diagnostic events
      tags: [Admin]
      responses:
        '200':
          description: Events log
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/DiagnosticEvent'

components:

  ###########################################################################
  # PARAMETERS
  ###########################################################################

  parameters:
    VehicleId:
      name: vehicleId
      in: path
      required: true
      schema: { type: string }

    JobId:
      name: jobId
      in: path
      required: true
      schema: { type: string }

    ApptId:
      name: apptId
      in: path
      required: true
      schema: { type: string }

  ###########################################################################
  # SCHEMAS
  ###########################################################################

  schemas:

    VehicleCreate:
      type: object
      properties:
        userId: { type: string }
        vin: { type: string }
        make: { type: string }
        model: { type: string }
        year: { type: integer }

    Vehicle:
      type: object
      properties:
        id: { type: string }
        userId: { type: string }
        vin: { type: string }
        make: { type: string }
        model: { type: string }
        year: { type: integer }
        healthStatus: { type: string }

    DiagnosticEvent:
      type: object
      properties:
        dongleId: { type: string }
        vehicleId: { type: string }
        timestamp: { type: string }
        codes:
          type: array
          items: { type: string }

    AIDiagnosisRequest:
      type: object
      properties:
        vehicleId: { type: string }
        codes:
          type: array
          items: { type: string }

    AIDiagnosis:
      type: object
      properties:
        primaryIssue: { type: string }
        recommendedRepairs:
          type: array
          items: { type: string }
        requiredParts:
          type: array
          items: { $ref: '#/components/schemas/PartItem' }
        severity: { type: string }

    PartItem:
      type: object
      properties:
        sku: { type: string }
        name: { type: string }
        supplier: { type: string }

    PartsOrderRequest:
      type: object
      properties:
        vehicleId: { type: string }
        parts:
          type: array
          items: { $ref: '#/components/schemas/PartItem' }

    PartsOrder:
      type: object
      properties:
        orderId: { type: string }
        status: { type: string }

    AutoScheduleRequest:
      type: object
      properties:
        vehicleId: { type: string }
        repairType: { type: string }

    AutoScheduleOptions:
      type: object
      properties:
        options:
          type: array
          items:
            type: object
            properties:
              slotId: { type: string }
              start: { type: string }
              end: { type: string }

    Appointment:
      type: object
      properties:
        id: { type: string }
        mechanicId: { type: string }
        start: { type: string }
        end: { type: string }

    Job:
      type: object
      properties:
        id: { type: string }
        vehicleId: { type: string }
        parts:
          type: array
          items: { $ref: '#/components/schemas/PartItem' }
        location: { type: string }
        scheduledTime: { type: string }

    ChargeRequest:
      type: object
      properties:
        userId: { type: string }
        amount: { type: number }
        jobId: { type: string }

    ChargeResult:
      type: object
      properties:
        status: { type: string }
        transactionId: { type: string }
