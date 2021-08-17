--
-- PostgreSQL database dump
--

-- Dumped from database version 12.7 (Debian 12.7-1.pgdg100+1)
-- Dumped by pg_dump version 13.4 (Ubuntu 13.4-1.pgdg20.04+1)

-- Started on 2021-08-16 13:22:34 +06

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 3 (class 2615 OID 2200)
-- Name: public; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA public;


ALTER SCHEMA public OWNER TO postgres;

--
-- TOC entry 2956 (class 0 OID 0)
-- Dependencies: 3
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON SCHEMA public IS 'standard public schema';


--
-- TOC entry 635 (class 1247 OID 16448)
-- Name: send_type_enum; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.send_type_enum AS ENUM (
    'send_type1',
    'send_type2',
    'send_type3'
);


ALTER TYPE public.send_type_enum OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 202 (class 1259 OID 16385)
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- TOC entry 204 (class 1259 OID 16416)
-- Name: ds_token_black_list; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ds_token_black_list (
    id uuid NOT NULL,
    jti character varying(36) NOT NULL,
    token_type character varying(10) NOT NULL,
    user_id uuid NOT NULL,
    revoked boolean NOT NULL,
    expires timestamp without time zone NOT NULL
);


ALTER TABLE public.ds_token_black_list OWNER TO postgres;

--
-- TOC entry 206 (class 1259 OID 16462)
-- Name: tbl_electronic_appeals; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tbl_electronic_appeals (
    id uuid NOT NULL,
    "externalRequestId" character varying(14) NOT NULL,
    id_user uuid NOT NULL,
    application_id uuid NOT NULL,
    descreption text NOT NULL,
    created_date timestamp with time zone,
    updated_date timestamp with time zone,
    response_appeal character varying(255)
);


ALTER TABLE public.tbl_electronic_appeals OWNER TO postgres;

--
-- TOC entry 203 (class 1259 OID 16390)
-- Name: tbl_users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tbl_users (
    id uuid NOT NULL,
    full_name character varying(255) NOT NULL,
    bin character varying(20) NOT NULL,
    mobile character varying(10) NOT NULL,
    email character varying(128),
    password character varying(255) NOT NULL,
    active boolean,
    update_time timestamp with time zone,
    create_time timestamp with time zone,
    photo character varying
);


ALTER TABLE public.tbl_users OWNER TO postgres;

--
-- TOC entry 205 (class 1259 OID 16455)
-- Name: tbl_verify_code; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tbl_verify_code (
    id uuid NOT NULL,
    mobile character varying(10) NOT NULL,
    code character varying(4) NOT NULL,
    send_type public.send_type_enum,
    create_time timestamp with time zone NOT NULL,
    repeat_count integer NOT NULL,
    repeat_expire_time timestamp with time zone
);


ALTER TABLE public.tbl_verify_code OWNER TO postgres;

--
-- TOC entry 2946 (class 0 OID 16385)
-- Dependencies: 202
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.alembic_version VALUES ('d3edfc59a690');


--
-- TOC entry 2948 (class 0 OID 16416)
-- Dependencies: 204
-- Data for Name: ds_token_black_list; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.ds_token_black_list VALUES ('3460a238-2443-463c-b22c-5c31d977cb6b', '902790b5-0832-4445-8ca8-0f8aa46ac820', 'refresh', '1e33d092-6fee-4ef2-91ac-d5872f7d7a68', false, '2021-09-10 10:31:32');
INSERT INTO public.ds_token_black_list VALUES ('cc6798fe-da64-47ee-8b9c-3127332f8903', 'ef3a8774-c6c3-4ecb-a252-51431c4c40fb', 'access', '1e33d092-6fee-4ef2-91ac-d5872f7d7a68', true, '2021-08-21 10:31:32');
INSERT INTO public.ds_token_black_list VALUES ('9c5ae1a5-0c31-4e6e-a3d8-1ae95c24e3c7', 'dd2e5290-78df-4308-baa9-50a482f27652', 'access', '1e33d092-6fee-4ef2-91ac-d5872f7d7a68', false, '2021-08-21 10:36:12');
INSERT INTO public.ds_token_black_list VALUES ('f37fa297-4b6b-4a29-849a-9f8072f31c17', '589e416b-f734-4c7e-a172-0c258a359fee', 'access', '1e33d092-6fee-4ef2-91ac-d5872f7d7a68', false, '2021-08-21 11:43:04');
INSERT INTO public.ds_token_black_list VALUES ('06035056-976a-4a0a-9800-f7ee3cd4f0d0', 'd5d7bc10-09c1-4966-ac59-b27dc22c4b82', 'refresh', '1e33d092-6fee-4ef2-91ac-d5872f7d7a68', false, '2021-09-10 11:43:04');
INSERT INTO public.ds_token_black_list VALUES ('da142a80-8e46-48f9-a068-2910886d2f14', '71de7220-86bc-4ceb-8b2c-17201bc5428c', 'access', '1e33d092-6fee-4ef2-91ac-d5872f7d7a68', false, '2021-08-22 19:22:25');
INSERT INTO public.ds_token_black_list VALUES ('9e39c532-4bc4-4422-84b1-82a8409a7e98', '944b43ff-0eb8-45fc-9d72-a12558d97b69', 'access', '1e33d092-6fee-4ef2-91ac-d5872f7d7a68', false, '2021-08-22 19:27:36');
INSERT INTO public.ds_token_black_list VALUES ('a0e4efaf-8eda-416e-8cdf-f0c5774e6b27', '495ac311-3773-4044-ae38-c96c8b24debb', 'access', '1e33d092-6fee-4ef2-91ac-d5872f7d7a68', false, '2021-08-23 04:33:37');
INSERT INTO public.ds_token_black_list VALUES ('8143f784-00bd-454f-a251-c8aff4c2b0ba', '15d2b87f-4530-4250-a582-e38f7e79a5b3', 'refresh', '1e33d092-6fee-4ef2-91ac-d5872f7d7a68', false, '2021-09-12 04:33:37');
INSERT INTO public.ds_token_black_list VALUES ('10247a2f-f2a1-430f-a0fe-b62551603bf3', 'c1ebbe60-4bb7-4011-af58-556a58d42c19', 'access', '1e33d092-6fee-4ef2-91ac-d5872f7d7a68', false, '2021-08-25 11:32:31');
INSERT INTO public.ds_token_black_list VALUES ('491a5f1f-2ddb-4f12-a480-a081a063b0fe', '631bddb9-8220-4391-81c7-323b972a94ea', 'refresh', '1e33d092-6fee-4ef2-91ac-d5872f7d7a68', false, '2021-09-14 11:32:31');
INSERT INTO public.ds_token_black_list VALUES ('8f4f64e3-a1b4-4441-9434-a541a765083c', 'ced73972-b3ed-4c55-b9b9-16212ec3d9b5', 'access', '1e33d092-6fee-4ef2-91ac-d5872f7d7a68', false, '2021-08-26 11:20:04');


--
-- TOC entry 2950 (class 0 OID 16462)
-- Dependencies: 206
-- Data for Name: tbl_electronic_appeals; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.tbl_electronic_appeals VALUES ('e6eaf34f-2cec-4848-9f32-bb374668237a', '10109001240440', '1e33d092-6fee-4ef2-91ac-d5872f7d7a68', 'ad202684-642a-41fe-9d17-c24e341fd699', 'Rakhmet jyldam qyzmet korsetkenderinizge!', '2021-08-16 13:15:25.00436+06', '2021-08-16 13:15:25.004393+06', NULL);


--
-- TOC entry 2947 (class 0 OID 16390)
-- Dependencies: 203
-- Data for Name: tbl_users; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.tbl_users VALUES ('457a0bbf-94a1-4a58-bb8a-d1c6a9ed4223', 'Bekzhan Rakhmetzhan', '891222456789', '7472095672', 'rakhmetzhan.bekzhan@mail.ru', '$pbkdf2-sha256$29000$rnXu3ds7p5RSijEGwFjrfQ$C6CJuGGL1RQC2LW8xsksaQTWY2J/6csin1MDFV2JX2M', true, '2021-08-12 11:50:26.921276+06', '2021-08-12 11:50:26.921297+06', NULL);
INSERT INTO public.tbl_users VALUES ('0053f09a-1b91-4d4e-992f-8a60f155eb94', 'Xxxxxxxxxxx yyyyyyyyyyy', '890512456123', '7007001455', 'xxx@mail.ru', '$pbkdf2-sha256$29000$3Lt3bg3hPCekFGKMcU6pFQ$BsYDBBOmhn9YjcbjMJqj2V3hwfxkucf7MpWR/Dp1994', true, '2021-08-13 14:50:02.083681+06', '2021-08-13 14:50:02.083701+06', NULL);
INSERT INTO public.tbl_users VALUES ('1e33d092-6fee-4ef2-91ac-d5872f7d7a68', 'Abilay Satibaldiev', '931227450493', '7007001466', 'haker3102@gmail.com', '$pbkdf2-sha256$29000$MWbMmZMyhvD.v9d6LyVEKA$rrxj4JkoGuQDJ1lP78OsLz6TXmlJJHigbOEmYKBsOb4', true, '2021-08-16 13:15:25.001408+06', '2021-08-05 10:39:06.01529+06', '44fa2ef2d85de8102a3a18abdc93e139c436c4df588888115ad4f543644fecb3.jpg');


--
-- TOC entry 2949 (class 0 OID 16455)
-- Dependencies: 205
-- Data for Name: tbl_verify_code; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.tbl_verify_code VALUES ('4232aef8-d3a5-44b4-9dba-36d44608aa2e', '7007001466', '740', 'send_type2', '2021-08-15 22:39:31.073314+06', 3, '2021-08-16 02:10:24.198548+06');


--
-- TOC entry 2797 (class 2606 OID 16389)
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- TOC entry 2807 (class 2606 OID 16422)
-- Name: ds_token_black_list ds_token_black_list_jti_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ds_token_black_list
    ADD CONSTRAINT ds_token_black_list_jti_key UNIQUE (jti);


--
-- TOC entry 2809 (class 2606 OID 16420)
-- Name: ds_token_black_list ds_token_black_list_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ds_token_black_list
    ADD CONSTRAINT ds_token_black_list_pkey PRIMARY KEY (id);


--
-- TOC entry 2799 (class 2606 OID 16399)
-- Name: tbl_users tbl_auth_service_users_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tbl_users
    ADD CONSTRAINT tbl_auth_service_users_email_key UNIQUE (email);


--
-- TOC entry 2801 (class 2606 OID 16401)
-- Name: tbl_users tbl_auth_service_users_mobile_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tbl_users
    ADD CONSTRAINT tbl_auth_service_users_mobile_key UNIQUE (mobile);


--
-- TOC entry 2803 (class 2606 OID 16397)
-- Name: tbl_users tbl_auth_service_users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tbl_users
    ADD CONSTRAINT tbl_auth_service_users_pkey PRIMARY KEY (id);


--
-- TOC entry 2815 (class 2606 OID 16471)
-- Name: tbl_electronic_appeals tbl_electronic_appeals_application_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tbl_electronic_appeals
    ADD CONSTRAINT tbl_electronic_appeals_application_id_key UNIQUE (application_id);


--
-- TOC entry 2817 (class 2606 OID 16469)
-- Name: tbl_electronic_appeals tbl_electronic_appeals_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tbl_electronic_appeals
    ADD CONSTRAINT tbl_electronic_appeals_pkey PRIMARY KEY (id);


--
-- TOC entry 2805 (class 2606 OID 16446)
-- Name: tbl_users tbl_users_bin_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tbl_users
    ADD CONSTRAINT tbl_users_bin_key UNIQUE (bin);


--
-- TOC entry 2811 (class 2606 OID 16461)
-- Name: tbl_verify_code tbl_verify_code_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tbl_verify_code
    ADD CONSTRAINT tbl_verify_code_id_key UNIQUE (id);


--
-- TOC entry 2813 (class 2606 OID 16459)
-- Name: tbl_verify_code tbl_verify_code_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tbl_verify_code
    ADD CONSTRAINT tbl_verify_code_pkey PRIMARY KEY (id);


--
-- TOC entry 2818 (class 2606 OID 16423)
-- Name: ds_token_black_list ds_token_black_list_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ds_token_black_list
    ADD CONSTRAINT ds_token_black_list_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.tbl_users(id);


--
-- TOC entry 2819 (class 2606 OID 16472)
-- Name: tbl_electronic_appeals tbl_electronic_appeals_id_user_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tbl_electronic_appeals
    ADD CONSTRAINT tbl_electronic_appeals_id_user_fkey FOREIGN KEY (id_user) REFERENCES public.tbl_users(id);


-- Completed on 2021-08-16 13:22:34 +06

--
-- PostgreSQL database dump complete
--

