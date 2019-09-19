GET CONNECTION FROM THE LOCAL POOL
CREATE TABLE "account_customer" (
  "id" SERIAL PRIMARY KEY,
  "insert_at" TIMESTAMP,
  "update_at" TIMESTAMP
)

CREATE TABLE "account_type" (
  "account_type" VARCHAR(20) PRIMARY KEY,
  "minimum_balance_restriction" DECIMAL(12, 2),
  "insert_at" TIMESTAMP,
  "update_at" TIMESTAMP
)

CREATE TABLE "address" (
  "address_id" SERIAL PRIMARY KEY,
  "street_address1" TEXT NOT NULL,
  "street_address2" TEXT NOT NULL,
  "city" VARCHAR(25) NOT NULL,
  "zipcode" VARCHAR(15) NOT NULL,
  "state" VARCHAR(45) NOT NULL,
  "country" VARCHAR(45) NOT NULL,
  "insert_at" TIMESTAMP,
  "update_at" TIMESTAMP
)

CREATE TABLE "cc_transaction" (
  "transaction_id" SERIAL PRIMARY KEY,
  "transaction_date" TIMESTAMP,
  "amount" DECIMAL(2, 2),
  "merchant_details" VARCHAR(100) NOT NULL,
  "insert_date" TIMESTAMP,
  "update_date" TIMESTAMP
)

CREATE TABLE "credit_card" (
  "cc_nmber" VARCHAR(20) PRIMARY KEY,
  "maximum_limit" DECIMAL(2, 2),
  "expiry_date" DATE,
  "credit_score" INTEGER,
  "insert_at" TIMESTAMP,
  "update_at" TIMESTAMP,
  "cc_transaction" INTEGER NOT NULL
)

CREATE INDEX "idx_credit_card__cc_transaction" ON "credit_card" ("cc_transaction")

ALTER TABLE "credit_card" ADD CONSTRAINT "fk_credit_card__cc_transaction" FOREIGN KEY ("cc_transaction") REFERENCES "cc_transaction" ("transaction_id") ON DELETE CASCADE

CREATE TABLE "employee" (
  "employee_id" SERIAL PRIMARY KEY,
  "level_of_access" VARCHAR(15) NOT NULL,
  "supervisor_id" INTEGER NOT NULL,
  "first_name" VARCHAR(45) NOT NULL,
  "last_name" VARCHAR(45) NOT NULL,
  "birth_of_date" DATE,
  "insert_at" TIMESTAMP,
  "update_at" TIMESTAMP,
  "address" INTEGER NOT NULL
)

CREATE INDEX "idx_employee__address" ON "employee" ("address")

CREATE INDEX "idx_employee__supervisor_id" ON "employee" ("supervisor_id")

ALTER TABLE "employee" ADD CONSTRAINT "fk_employee__address" FOREIGN KEY ("address") REFERENCES "address" ("address_id") ON DELETE CASCADE

ALTER TABLE "employee" ADD CONSTRAINT "fk_employee__supervisor_id" FOREIGN KEY ("supervisor_id") REFERENCES "employee" ("employee_id") ON DELETE CASCADE

CREATE TABLE "loan" (
  "loan_id" SERIAL PRIMARY KEY,
  "duration_in_years" INTEGER,
  "loan_start_date" DATE,
  "interest_rate" DOUBLE PRECISION,
  "loan_amount_taken" DECIMAL(2, 2),
  "loan_amount_repaid" DECIMAL(2, 2),
  "loan_type" VARCHAR(45) NOT NULL,
  "inset_at" TIMESTAMP,
  "update_at" TIMESTAMP
)

CREATE TABLE "transaction_types" (
  "transaction_type_code" VARCHAR(25) PRIMARY KEY,
  "transaction_type_description" TEXT NOT NULL,
  "insert_at" TIMESTAMP,
  "update_at" TIMESTAMP
)

CREATE TABLE "bank_transaction" (
  "transaction_id" SERIAL PRIMARY KEY,
  "maximum_limit" DECIMAL(12, 2),
  "description" TEXT NOT NULL,
  "transaction_date" TIMESTAMP,
  "transaction_types" VARCHAR(25) NOT NULL
)

CREATE INDEX "idx_bank_transaction__transaction_types" ON "bank_transaction" ("transaction_types")

ALTER TABLE "bank_transaction" ADD CONSTRAINT "fk_bank_transaction__transaction_types" FOREIGN KEY ("transaction_types") REFERENCES "transaction_types" ("transaction_type_code") ON DELETE CASCADE

CREATE TABLE "branches" (
  "branch_id" SERIAL PRIMARY KEY,
  "branch_name" VARCHAR(45) NOT NULL,
  "phone_number" VARCHAR(12) NOT NULL,
  "insert_at" TIMESTAMP,
  "update_at" TIMESTAMP,
  "bank_transaction" INTEGER NOT NULL
)

CREATE INDEX "idx_branches__bank_transaction" ON "branches" ("bank_transaction")

ALTER TABLE "branches" ADD CONSTRAINT "fk_branches__bank_transaction" FOREIGN KEY ("bank_transaction") REFERENCES "bank_transaction" ("transaction_id") ON DELETE CASCADE

CREATE TABLE "account" (
  "account_id" SERIAL PRIMARY KEY,
  "account_balance" DECIMAL(12, 2),
  "branches" INTEGER NOT NULL,
  "date_opened" DATE,
  "account_type" VARCHAR(20) NOT NULL,
  "insert_at" TIMESTAMP,
  "update_at" TIMESTAMP,
  "account_customer" INTEGER NOT NULL
)

CREATE INDEX "idx_account__account_customer" ON "account" ("account_customer")

CREATE INDEX "idx_account__account_type" ON "account" ("account_type")

CREATE INDEX "idx_account__branches" ON "account" ("branches")

ALTER TABLE "account" ADD CONSTRAINT "fk_account__account_customer" FOREIGN KEY ("account_customer") REFERENCES "account_customer" ("id") ON DELETE CASCADE

ALTER TABLE "account" ADD CONSTRAINT "fk_account__account_type" FOREIGN KEY ("account_type") REFERENCES "account_type" ("account_type") ON DELETE CASCADE

ALTER TABLE "account" ADD CONSTRAINT "fk_account__branches" FOREIGN KEY ("branches") REFERENCES "branches" ("branch_id") ON DELETE CASCADE

CREATE TABLE "branches_employees" (
  "id" SERIAL PRIMARY KEY,
  "branches" INTEGER NOT NULL,
  "start_date" DATE,
  "end_date" DATE,
  "minimum_balance_restriction" DECIMAL(12, 2),
  "insert_at" TIMESTAMP,
  "update_at" TIMESTAMP,
  "employee" INTEGER NOT NULL
)

CREATE INDEX "idx_branches_employees__branches" ON "branches_employees" ("branches")

CREATE INDEX "idx_branches_employees__employee" ON "branches_employees" ("employee")

ALTER TABLE "branches_employees" ADD CONSTRAINT "fk_branches_employees__branches" FOREIGN KEY ("branches") REFERENCES "branches" ("branch_id") ON DELETE CASCADE

ALTER TABLE "branches_employees" ADD CONSTRAINT "fk_branches_employees__employee" FOREIGN KEY ("employee") REFERENCES "employee" ("employee_id") ON DELETE CASCADE

CREATE TABLE "customer" (
  "customer_id" SERIAL PRIMARY KEY,
  "first_name" VARCHAR(45) NOT NULL,
  "last_name" VARCHAR(45) NOT NULL,
  "date_of_birth" DATE,
  "email" VARCHAR(55) NOT NULL,
  "insert_at" TIMESTAMP,
  "update_at" TIMESTAMP,
  "account_customer" INTEGER NOT NULL,
  "bank_transaction" INTEGER NOT NULL,
  "credit_card" VARCHAR(20) NOT NULL,
  "loan" INTEGER NOT NULL,
  "address" INTEGER NOT NULL
)

CREATE INDEX "idx_customer__account_customer" ON "customer" ("account_customer")

CREATE INDEX "idx_customer__address" ON "customer" ("address")

CREATE INDEX "idx_customer__bank_transaction" ON "customer" ("bank_transaction")

CREATE INDEX "idx_customer__credit_card" ON "customer" ("credit_card")

CREATE INDEX "idx_customer__loan" ON "customer" ("loan")

ALTER TABLE "customer" ADD CONSTRAINT "fk_customer__account_customer" FOREIGN KEY ("account_customer") REFERENCES "account_customer" ("id") ON DELETE CASCADE

ALTER TABLE "customer" ADD CONSTRAINT "fk_customer__address" FOREIGN KEY ("address") REFERENCES "address" ("address_id") ON DELETE CASCADE

ALTER TABLE "customer" ADD CONSTRAINT "fk_customer__bank_transaction" FOREIGN KEY ("bank_transaction") REFERENCES "bank_transaction" ("transaction_id") ON DELETE CASCADE

ALTER TABLE "customer" ADD CONSTRAINT "fk_customer__credit_card" FOREIGN KEY ("credit_card") REFERENCES "credit_card" ("cc_nmber") ON DELETE CASCADE

ALTER TABLE "customer" ADD CONSTRAINT "fk_customer__loan" FOREIGN KEY ("loan") REFERENCES "loan" ("loan_id") ON DELETE CASCADE

SELECT "account"."account_id", "account"."account_balance", "account"."branches", "account"."date_opened", "account"."account_type", "account"."insert_at", "account"."update_at", "account"."account_customer"
FROM "account" "account"
WHERE 0 = 1

SELECT "account_customer"."id", "account_customer"."insert_at", "account_customer"."update_at"
FROM "account_customer" "account_customer"
WHERE 0 = 1

SELECT "account_type"."account_type", "account_type"."minimum_balance_restriction", "account_type"."insert_at", "account_type"."update_at"
FROM "account_type" "account_type"
WHERE 0 = 1

SELECT "address"."address_id", "address"."street_address1", "address"."street_address2", "address"."city", "address"."zipcode", "address"."state", "address"."country", "address"."insert_at", "address"."update_at"
FROM "address" "address"
WHERE 0 = 1

SELECT "bank_transaction"."transaction_id", "bank_transaction"."maximum_limit", "bank_transaction"."description", "bank_transaction"."transaction_date", "bank_transaction"."transaction_types"
FROM "bank_transaction" "bank_transaction"
WHERE 0 = 1

SELECT "branches"."branch_id", "branches"."branch_name", "branches"."phone_number", "branches"."insert_at", "branches"."update_at", "branches"."bank_transaction"
FROM "branches" "branches"
WHERE 0 = 1

SELECT "branches_employees"."id", "branches_employees"."branches", "branches_employees"."start_date", "branches_employees"."end_date", "branches_employees"."minimum_balance_restriction", "branches_employees"."insert_at", "branches_employees"."update_at", "branches_employees"."employee"
FROM "branches_employees" "branches_employees"
WHERE 0 = 1

SELECT "cc_transaction"."transaction_id", "cc_transaction"."transaction_date", "cc_transaction"."amount", "cc_transaction"."merchant_details", "cc_transaction"."insert_date", "cc_transaction"."update_date"
FROM "cc_transaction" "cc_transaction"
WHERE 0 = 1

SELECT "credit_card"."cc_nmber", "credit_card"."maximum_limit", "credit_card"."expiry_date", "credit_card"."credit_score", "credit_card"."insert_at", "credit_card"."update_at", "credit_card"."cc_transaction"
FROM "credit_card" "credit_card"
WHERE 0 = 1

SELECT "customer"."customer_id", "customer"."first_name", "customer"."last_name", "customer"."date_of_birth", "customer"."email", "customer"."insert_at", "customer"."update_at", "customer"."account_customer", "customer"."bank_transaction", "customer"."credit_card", "customer"."loan", "customer"."address"
FROM "customer" "customer"
WHERE 0 = 1

SELECT "employee"."employee_id", "employee"."level_of_access", "employee"."supervisor_id", "employee"."first_name", "employee"."last_name", "employee"."birth_of_date", "employee"."insert_at", "employee"."update_at", "employee"."address"
FROM "employee" "employee"
WHERE 0 = 1

SELECT "loan"."loan_id", "loan"."duration_in_years", "loan"."loan_start_date", "loan"."interest_rate", "loan"."loan_amount_taken", "loan"."loan_amount_repaid", "loan"."loan_type", "loan"."inset_at", "loan"."update_at"
FROM "loan" "loan"
WHERE 0 = 1

SELECT "transaction_types"."transaction_type_code", "transaction_types"."transaction_type_description", "transaction_types"."insert_at", "transaction_types"."update_at"
FROM "transaction_types" "transaction_types"
WHERE 0 = 1

COMMIT
CLOSE CONNECTION
