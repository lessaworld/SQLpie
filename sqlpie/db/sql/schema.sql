
CREATE TABLE buckets (
 id                        INT    UNSIGNED        NOT NULL AUTO_INCREMENT PRIMARY KEY,
 bucket                    VARCHAR(255)        NOT NULL,
 bucket_id                BINARY(20)            NOT NULL,
 doc_count                INT UNSIGNED        NOT NULL DEFAULT 1,
 UNIQUE KEY (bucket_id)
) ENGINE=InnoDB CHARSET=utf8 COLLATE=utf8_unicode_ci;

CREATE TABLE documents(
 id                        INT    UNSIGNED        NOT NULL AUTO_INCREMENT PRIMARY KEY,
 bucket_id                BINARY(20)            NOT NULL,
 document_id            BINARY(20)            NOT NULL,
 document                MEDIUMTEXT            NOT NULL,
 is_compressed          BOOLEAN             NOT NULL,
 state                    TINYINT UNSIGNED    NOT NULL DEFAULT 0,
 created_at                TIMESTAMP             NOT NULL,
 tdidf_score            DOUBLE                NULL,
 UNIQUE KEY (bucket_id, document_id),
 INDEX `idx_documents_state` (`state`)
) ENGINE=InnoDB CHARSET=utf8 COLLATE=utf8_unicode_ci;

CREATE TABLE content_keys (
 id                        INT    UNSIGNED        NOT NULL AUTO_INCREMENT PRIMARY KEY,
 content_key            VARCHAR(2048)        NOT NULL,
 key_id                    BINARY(20)            NOT NULL,
 key_count                INT UNSIGNED        NOT NULL  DEFAULT 1,
 UNIQUE KEY (key_id)
) ENGINE=InnoDB CHARSET=utf8 COLLATE=utf8_unicode_ci;

CREATE TABLE contents (
 id                        INT    UNSIGNED        NOT NULL AUTO_INCREMENT PRIMARY KEY,
 bucket_id                BINARY(20)            NOT    NULL,
 document_id             BINARY(20)             NOT NULL,
 key_id                    BINARY(20)            NOT NULL,
 content_type            TINYINT UNSIGNED    NOT NULL,
 value                    VARCHAR(16384)        NOT NULL,
 numeric_value            DOUBLE                NULL,
 INDEX `idx_contents_bucket_id_and_document_id` (`bucket_id`, `document_id`),
 INDEX `idx_contents_key_id_numeric_value` (`key_id`, `numeric_value`)
) ENGINE=InnoDB CHARSET=utf8 COLLATE=utf8_unicode_ci;

CREATE TABLE terms (
  id                    INT UNSIGNED        NOT NULL  AUTO_INCREMENT PRIMARY KEY,
  bucket_id                BINARY(20)            NOT NULL,
  term_id                BINARY(20)            NOT NULL,
  term_count            INT UNSIGNED        NOT NULL DEFAULT 1,
  UNIQUE KEY (bucket_id, term_id)
) ENGINE=InnoDB CHARSET=utf8 COLLATE=utf8_unicode_ci;

CREATE TABLE content_terms(
  id                    INT UNSIGNED        NOT NULL  AUTO_INCREMENT PRIMARY KEY,
  bucket_id                BINARY(20)            NOT NULL,
  document_id             BINARY(20)             NOT NULL,
  key_id                BINARY(20)            NOT NULL,
  term_id                BINARY(20)            NOT NULL,
  term_pos                INT UNSIGNED        NOT NULL,
  original                VARCHAR(255)        NOT NULL,
  INDEX `idx_contents_bucket_id_and_document_id_and_key_id` (`bucket_id`, `document_id`, `key_id`, `term_id`, `term_pos`)
) ENGINE=InnoDB CHARSET=utf8 COLLATE=utf8_unicode_ci;

CREATE TABLE ranking_tf(
  id                    INT UNSIGNED        NOT NULL  AUTO_INCREMENT PRIMARY KEY,
  bucket_id                BINARY(20)            NOT NULL,
  document_id             BINARY(20)             NOT NULL,
  term_id                BINARY(20)            NOT NULL,
  normalized_frequency    FLOAT                NOT NULL DEFAULT 0
) ENGINE=InnoDB CHARSET=utf8 COLLATE=utf8_unicode_ci;

CREATE TABLE ranking_idf(
  id                    INT UNSIGNED        NOT NULL  AUTO_INCREMENT PRIMARY KEY,
  bucket_id                BINARY(20)            NOT NULL,
  term_id                BINARY(20)            NOT NULL,
  num_doc                INT                    NOT NULL DEFAULT 1,
  frequency                FLOAT                NOT NULL DEFAULT 0,
  UNIQUE KEY (bucket_id, term_id)
) ENGINE=InnoDB CHARSET=utf8 COLLATE=utf8_unicode_ci;

CREATE TABLE predicates (
 id                        INT    UNSIGNED        NOT NULL AUTO_INCREMENT PRIMARY KEY,
 predicate                VARCHAR(255)        NOT NULL,
 predicate_id            BINARY(20)            NOT NULL,
 observation_count        INT UNSIGNED        NOT NULL DEFAULT 1,
 UNIQUE KEY (predicate_id)
) ENGINE=InnoDB CHARSET=utf8 COLLATE=utf8_unicode_ci;

CREATE TABLE observations(
  id                    INT    UNSIGNED        NOT NULL AUTO_INCREMENT PRIMARY KEY,
  created_at            TIMESTAMP             NOT NULL,
  subject_bucket_id        BINARY(20)            NOT NULL,
  subject_id            BINARY(20)            NOT NULL,
  object_bucket_id        BINARY(20)            NOT NULL,
  object_id                BINARY(20)            NOT NULL,
  predicate_id            BINARY(20)            NOT NULL,
  predicate_type        TINYINT UNSIGNED    NOT NULL,
  predicate_value        VARCHAR(2048)        NULL,
  observation            MEDIUMTEXT            NOT NULL,
  is_compressed          BOOLEAN             NOT NULL,
  INDEX `idx_observations_predicate` (`created_at`, `predicate_id`),
  INDEX `idx_observations_subject` (`created_at`, `subject_bucket_id`,`subject_id`),
  INDEX `idx_observations_object` (`created_at`, `object_bucket_id`,`object_id`)
) ENGINE=InnoDB CHARSET=utf8 COLLATE=utf8_unicode_ci;

CREATE TABLE caches(
  id                    INT    UNSIGNED        NOT NULL AUTO_INCREMENT PRIMARY KEY,
  bucket_id                BINARY(20)            NOT NULL,
  key_id                BINARY(20)            NOT NULL,
  expire_at                TIMESTAMP             NOT NULL,
  cache_key                VARCHAR(2048)        NOT NULL,
  value                    VARCHAR(2048)        NULL,
  UNIQUE KEY (bucket_id, key_id)
) ENGINE=InnoDB CHARSET=utf8 COLLATE=utf8_unicode_ci;


CREATE TABLE `geo_documents` (
  `id`                     INT UNSIGNED         NOT NULL AUTO_INCREMENT,
  `bucket_id`             BINARY(20)             NOT NULL,
  `document_id`            BINARY(20)             NOT NULL,
  `latitude`             DOUBLE(9,6)         NOT NULL,
  `longitude`             DOUBLE(9,6)         NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY (bucket_id, document_id),
  KEY `idx_geo_documents_lat_long` (`latitude`,`longitude`)
) ENGINE=InnoDB CHARSET=utf8 COLLATE=utf8_unicode_ci;

CREATE TABLE `models` (
  `id`                     INT UNSIGNED         NOT NULL AUTO_INCREMENT,
  `bucket`                VARCHAR(255)         NOT NULL,
  `predicate`            VARCHAR(255)         NOT NULL,
  `model`                 VARCHAR(255)         NOT NULL,
  `bucket_id`             BINARY(20)             NOT NULL,
  `predicate_id`        BINARY(20)             NOT NULL,
  `model_id`            BINARY(20)             NOT NULL,
  `last_observation`     TIMESTAMP             NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY (`model_id`)
) ENGINE=InnoDB CHARSET=utf8 COLLATE=utf8_unicode_ci;

CREATE TABLE `model_classifiers` (
  `id`                     INT UNSIGNED         NOT NULL AUTO_INCREMENT,
  `model_id`             BINARY(20)             NOT NULL,
  `subject_id`            BINARY(20)             NOT NULL,
  `score_type`            TINYINT UNSIGNED    NOT NULL,
  `score`                  FLOAT                NOT NULL DEFAULT 1,
  `label`                VARCHAR(255)        NOT NULL,
  `feature`                VARCHAR(255)        NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY (`model_id`,`subject_id`,`label`,`feature`),
  KEY `idx_labels` (`model_id`,`subject_id`,`feature`)
) ENGINE=InnoDB CHARSET=utf8 COLLATE=utf8_unicode_ci;

CREATE TABLE `schema` (
  `id`                     INT(10) UNSIGNED     NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `version`             VARCHAR(255)        NOT NULL
) ENGINE=InnoDB CHARSET=utf8 COLLATE=utf8_unicode_ci;
