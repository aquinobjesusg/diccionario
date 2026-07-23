--
-- PostgreSQL database dump
--



--
-- TOC entry 228 (class 1259 OID 16825)
-- Name: diccionario_base; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.diccionario_base (
    id_diccionario_base integer NOT NULL,
    id_tipo_archivo integer,
    id_nivel integer,
    id_lenguaje_1 integer,
    id_lenguaje_2 integer,
    id_tipo_palabra integer
);



--
-- TOC entry 227 (class 1259 OID 16824)
-- Name: diccionario_base_id_diccionario_base_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.diccionario_base_id_diccionario_base_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;




--
-- TOC entry 5138 (class 0 OID 0)
-- Dependencies: 227
-- Name: diccionario_base_id_diccionario_base_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.diccionario_base_id_diccionario_base_seq OWNED BY public.diccionario_base.id_diccionario_base;


--
-- TOC entry 230 (class 1259 OID 16858)
-- Name: diccionario_uso; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.diccionario_uso (
    id_registro integer NOT NULL,
    id_diccionario_base integer,
    id_elemento_1 integer,
    id_elemento_2 integer
);




--
-- TOC entry 229 (class 1259 OID 16857)
-- Name: diccionario_uso_id_registro_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.diccionario_uso_id_registro_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;




--
-- TOC entry 5139 (class 0 OID 0)
-- Dependencies: 229
-- Name: diccionario_uso_id_registro_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.diccionario_uso_id_registro_seq OWNED BY public.diccionario_uso.id_registro;


--
-- TOC entry 220 (class 1259 OID 16725)
-- Name: lenguajes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.lenguajes (
    id_lenguaje integer NOT NULL,
    lenguaje character varying(100) NOT NULL
);




--
-- TOC entry 219 (class 1259 OID 16724)
-- Name: lenguajes_id_lenguaje_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.lenguajes_id_lenguaje_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;




--
-- TOC entry 5140 (class 0 OID 0)
-- Dependencies: 219
-- Name: lenguajes_id_lenguaje_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.lenguajes_id_lenguaje_seq OWNED BY public.lenguajes.id_lenguaje;


--
-- TOC entry 234 (class 1259 OID 24611)
-- Name: modismos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.modismos (
    id_modismo integer NOT NULL,
    id_lenguaje integer NOT NULL,
    id_nivel integer,
    modismo text
);




--
-- TOC entry 222 (class 1259 OID 16734)
-- Name: nivel; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.nivel (
    id_nivel integer NOT NULL,
    nivel character varying(50) NOT NULL
);




--
-- TOC entry 221 (class 1259 OID 16733)
-- Name: nivel_id_nivel_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.nivel_id_nivel_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;




--
-- TOC entry 5141 (class 0 OID 0)
-- Dependencies: 221
-- Name: nivel_id_nivel_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.nivel_id_nivel_seq OWNED BY public.nivel.id_nivel;


--
-- TOC entry 232 (class 1259 OID 24581)
-- Name: paises; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.paises (
    id_pais integer NOT NULL,
    pais character varying(100) NOT NULL
);




--
-- TOC entry 231 (class 1259 OID 24580)
-- Name: paises_id_pais_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.paises_id_pais_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;




--
-- TOC entry 5142 (class 0 OID 0)
-- Dependencies: 231
-- Name: paises_id_pais_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.paises_id_pais_seq OWNED BY public.paises.id_pais;


--
-- TOC entry 233 (class 1259 OID 24604)
-- Name: palabras; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.palabras (
    id_palabra integer NOT NULL,
    id_lenguaje integer NOT NULL,
    id_tipo_palabra integer,
    id_nivel integer,
    palabra character varying(100),
    subtipo integer DEFAULT 1
);




--
-- TOC entry 239 (class 1259 OID 24748)
-- Name: sesion_usuario; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.sesion_usuario (
    id integer NOT NULL,
    usuario_id text DEFAULT 'unico'::text,
    menu_actual text NOT NULL,
    jugando integer NOT NULL,
    mod_j text,
    ord_j text,
    ayuda_juego text,
    aciertos integer DEFAULT 0,
    fallos integer DEFAULT 0,
    c_idx integer DEFAULT 0,
    j_paso integer DEFAULT 1,
    j_status text,
    j_indices text,
    j_vistos text,
    j_fallidos_json text,
    fecha_guardado timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);




--
-- TOC entry 238 (class 1259 OID 24747)
-- Name: sesion_usuario_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.sesion_usuario_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;




--
-- TOC entry 5143 (class 0 OID 0)
-- Dependencies: 238
-- Name: sesion_usuario_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.sesion_usuario_id_seq OWNED BY public.sesion_usuario.id;


--
-- TOC entry 226 (class 1259 OID 16752)
-- Name: tipo_palabra; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tipo_palabra (
    id_tipo_palabra integer NOT NULL,
    tipo_palabra character varying(100) NOT NULL
);




--
-- TOC entry 225 (class 1259 OID 16751)
-- Name: tipo_palabra_id_tipo_palabra_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tipo_palabra_id_tipo_palabra_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;




--
-- TOC entry 5144 (class 0 OID 0)
-- Dependencies: 225
-- Name: tipo_palabra_id_tipo_palabra_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tipo_palabra_id_tipo_palabra_seq OWNED BY public.tipo_palabra.id_tipo_palabra;


--
-- TOC entry 224 (class 1259 OID 16743)
-- Name: tipos_archivo; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tipos_archivo (
    id_tipo_archivo integer NOT NULL,
    tipo_archivo character varying(100) NOT NULL
);




--
-- TOC entry 223 (class 1259 OID 16742)
-- Name: tipos_archivo_id_tipo_archivo_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tipos_archivo_id_tipo_archivo_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;




--
-- TOC entry 5145 (class 0 OID 0)
-- Dependencies: 223
-- Name: tipos_archivo_id_tipo_archivo_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tipos_archivo_id_tipo_archivo_seq OWNED BY public.tipos_archivo.id_tipo_archivo;


--
-- TOC entry 237 (class 1259 OID 24721)
-- Name: usuarios; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.usuarios (
    id_usuario integer NOT NULL,
    nombre character varying(100) NOT NULL,
    correo character varying(150) NOT NULL,
    alias character varying(50) NOT NULL,
    nivel character varying(50) NOT NULL,
    clave text,
    token_verificacion text,
    fecha_registro timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    ultimo_cambio_pwd timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    estado character varying(20) DEFAULT 'PENDIENTE'::character varying,
    intentos_fallidos integer DEFAULT 0,
    es_admin boolean DEFAULT false
);




--
-- TOC entry 236 (class 1259 OID 24720)
-- Name: usuarios_id_usuario_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.usuarios_id_usuario_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;




--
-- TOC entry 5146 (class 0 OID 0)
-- Dependencies: 236
-- Name: usuarios_id_usuario_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.usuarios_id_usuario_seq OWNED BY public.usuarios.id_usuario;


--
-- TOC entry 235 (class 1259 OID 24621)
-- Name: verbos_compuestos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.verbos_compuestos (
    id_verbo integer NOT NULL,
    id_lenguaje integer NOT NULL,
    id_nivel integer,
    verbo text
);




--
-- TOC entry 4912 (class 2604 OID 16828)
-- Name: diccionario_base id_diccionario_base; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.diccionario_base ALTER COLUMN id_diccionario_base SET DEFAULT nextval('public.diccionario_base_id_diccionario_base_seq'::regclass);


--
-- TOC entry 4913 (class 2604 OID 16861)
-- Name: diccionario_uso id_registro; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.diccionario_uso ALTER COLUMN id_registro SET DEFAULT nextval('public.diccionario_uso_id_registro_seq'::regclass);


--
-- TOC entry 4908 (class 2604 OID 16728)
-- Name: lenguajes id_lenguaje; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.lenguajes ALTER COLUMN id_lenguaje SET DEFAULT nextval('public.lenguajes_id_lenguaje_seq'::regclass);


--
-- TOC entry 4909 (class 2604 OID 16737)
-- Name: nivel id_nivel; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.nivel ALTER COLUMN id_nivel SET DEFAULT nextval('public.nivel_id_nivel_seq'::regclass);


--
-- TOC entry 4914 (class 2604 OID 24584)
-- Name: paises id_pais; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.paises ALTER COLUMN id_pais SET DEFAULT nextval('public.paises_id_pais_seq'::regclass);


--
-- TOC entry 4922 (class 2604 OID 24751)
-- Name: sesion_usuario id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sesion_usuario ALTER COLUMN id SET DEFAULT nextval('public.sesion_usuario_id_seq'::regclass);


--
-- TOC entry 4911 (class 2604 OID 16755)
-- Name: tipo_palabra id_tipo_palabra; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tipo_palabra ALTER COLUMN id_tipo_palabra SET DEFAULT nextval('public.tipo_palabra_id_tipo_palabra_seq'::regclass);


--
-- TOC entry 4910 (class 2604 OID 16746)
-- Name: tipos_archivo id_tipo_archivo; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tipos_archivo ALTER COLUMN id_tipo_archivo SET DEFAULT nextval('public.tipos_archivo_id_tipo_archivo_seq'::regclass);


--
-- TOC entry 4916 (class 2604 OID 24724)
-- Name: usuarios id_usuario; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios ALTER COLUMN id_usuario SET DEFAULT nextval('public.usuarios_id_usuario_seq'::regclass);


--
-- TOC entry 5121 (class 0 OID 16825)
-- Dependencies: 228
-- Data for Name: diccionario_base; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.diccionario_base (id_diccionario_base, id_tipo_archivo, id_nivel, id_lenguaje_1, id_lenguaje_2, id_tipo_palabra) FROM stdin;
\.


--
-- TOC entry 5123 (class 0 OID 16858)
-- Dependencies: 230
-- Data for Name: diccionario_uso; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.diccionario_uso (id_registro, id_diccionario_base, id_elemento_1, id_elemento_2) FROM stdin;
\.


--
-- TOC entry 5113 (class 0 OID 16725)
-- Dependencies: 220
-- Data for Name: lenguajes; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.lenguajes (id_lenguaje, lenguaje) FROM stdin;
1	Inglés
2	Español
3	Portugués
4	Francés
5	Alemán
6	Italiano
7	Chino
8	Japonés
9	Ruso
10	Coreano
\.


--
-- TOC entry 5127 (class 0 OID 24611)
-- Dependencies: 234
-- Data for Name: modismos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.modismos (id_modismo, id_lenguaje, id_nivel, modismo) FROM stdin;
101	1	2	To be in the same boat
101	2	2	Estar en el mismo barco
102	1	2	To be on cloud nine
102	2	2	Estar en el séptimo cielo / Muy feliz
103	1	2	To bell the cat
103	2	2	Ponerle el cascabel al gato
104	1	2	To blow your own trumpet
104	2	2	Darse pote / Alardear
105	1	2	To bring home the bacon
105	2	2	Traer el pan a casa / Ganar el sustento
106	1	2	To butter someone up
106	2	2	Hacer la pelota / Adular a alguien
107	1	2	To catch someone red-handed
107	2	2	Pillar a alguien con las manos en la masa
108	1	2	To drive someone up the wall
108	2	2	Sacar a alguien de quicio
109	1	2	To eat humble pie
109	2	2	Tragar saliva / Reconocer un error
110	1	2	To feel like a fish out of water
110	2	2	Sentirse como un pulpo en un garaje
111	1	2	To get the hang of something
111	2	2	Pillarle el truco a algo
112	1	2	To give someone a hand
112	2	2	Echar una mano a alguien
113	1	2	To have a bone to pick with someone
113	2	2	Tener cuentas que ajustar con alguien
114	1	2	To have other fish to fry
114	2	2	Tener otros asuntos que atender
115	1	2	To hit the jackpot
115	2	2	Llevarse el premio gordo
116	1	2	To keep a straight face
116	2	2	Mantener la compostura / No reírse
117	1	2	To kick the bucket
117	2	2	Estirar la pata / Morir
118	1	2	To kill time
118	2	2	Matar el tiempo
119	1	2	To let the steam off
119	2	2	Desahogarse
120	1	2	To make a mountain out of a molehill
120	2	2	Hacer una montaña de un grano de arena
121	1	2	To pay through the nose
121	2	2	Pagar un ojo de la cara
122	1	2	To pull out all the stops
122	2	2	Echar el resto / Hacer todo lo posible
123	1	2	To put your foot in it
123	2	2	Meter la pata
124	1	2	To rain cats and dogs
124	2	2	Llover a cántaros
125	1	2	To read between the lines
125	2	2	Leer entre líneas
126	1	2	To rock the boat
126	2	2	Trastocar los planes / Crear problemas
127	1	2	To rub salt in the wound
127	2	2	Hurgar en la herida
128	1	2	To smell a rat
128	2	2	Olerse algo chamuscado
129	1	2	To spill the beans
129	2	2	Irse de la lengua
130	1	2	To take the bull by the horns
130	2	2	Coger el toro por los cuernos
131	1	2	To turn a blind eye
131	2	2	Hacer la vista gorda
132	1	2	To weather the storm
132	2	2	Capear el temporal
133	1	2	A cold day in hell
133	2	2	Cuando las ranas críen pelo
134	1	2	A house of cards
134	2	2	Un castillo de naipes
135	1	2	A leopards spots
135	2	2	Genio y figura hasta la sepultura
136	1	2	A litmus test
136	2	2	La prueba de fuego
137	1	2	A stone’s throw
137	2	2	A tiro de piedra / Muy cerca
138	1	2	All ears
138	2	2	Ser todo oídos
139	1	2	All in a day’s work
139	2	2	Gajes del oficio
140	1	2	All over the place
140	2	2	Por todas partes / Desordenado
141	1	2	An armchair critic
141	2	2	Un opinólogo / Alguien que critica sin saber
142	1	2	At the end of your tether
142	2	2	Estar al límite de la paciencia
143	1	2	Back to the drawing board
143	2	2	Empezar de nuevo desde cero
144	1	2	Barking up the wrong tree
144	2	2	Estar equivocado de cabo a rabo
145	1	2	Beating a dead horse
145	2	2	Perder el tiempo en algo sin solución
146	1	2	Behind the times
146	2	2	Anticuado
147	1	2	Bells and whistles
147	2	2	Adornos / Funciones extra
148	1	2	Beside oneself
148	2	2	Fuera de sí
149	1	2	Between a rock and a hard place
149	2	2	Entre la espada y la pared
150	1	2	Big fish in a small pond
150	2	2	Pez gordo en pecera pequeña
151	1	2	Bird’s eye view
151	2	2	A vista de pájaro
152	1	2	Bite the hand that feeds you
152	2	2	Morder la mano que te da de comer
153	1	2	Blood is thicker than water
153	2	2	La familia es lo primero
154	1	2	Bob’s your uncle
154	2	2	Y listo / Así de fácil
155	1	2	Bolt from the blue
155	2	2	Como un balde de agua fría
156	1	2	Born with a silver spoon
156	2	2	Nacer en cuna de oro
157	1	2	Building castles in the air
157	2	2	Hacer castillos en el aire
158	1	2	Burning the candle at both ends
158	2	2	Agotarse por trabajar demasiado
159	1	2	By the book
159	2	2	Según las reglas / Al pie de la letra
160	1	2	Carry the can
160	2	2	Cargar con las culpas
161	1	2	Change of heart
161	2	2	Cambio de parecer
162	1	2	Chicken out
162	2	2	Acobardarse
163	1	2	Chip on your shoulder
163	2	2	Tener un resentimiento
164	1	2	Clean bill of health
164	2	2	Certificado de buena salud
165	1	2	Close but no cigar
165	2	2	Cerca, pero no lo suficiente
166	1	2	Come rain or shine
166	2	2	Pase lo que pase
167	1	2	Cooking the books
167	2	2	Falsear las cuentas
168	1	2	Crocodile tears
168	2	2	Lágrimas de cocodrilo
169	1	2	Cry wolf
169	2	2	Dar una falsa alarma
170	1	2	Curiosity killed the cat
170	2	2	La curiosidad mató al gato
171	1	2	Dead ringer
171	2	2	Ser la viva imagen de alguien
172	1	2	Dog days of summer
172	2	2	Los días de canícula / Calor extremo
173	1	2	Don’t hold your breath
173	2	2	No esperes sentado
174	1	2	Double edged sword
174	2	2	Arma de doble filo
175	1	2	Down to earth
175	2	2	Tener los pies en la tierra
176	1	2	Draw the line
176	2	2	Poner un límite
177	1	2	Dress to kill
177	2	2	Vestirse para impresionar
178	1	2	Drop in the ocean
178	2	2	Una gota en el mar
179	1	2	Each to their own
179	2	2	Cada loco con su tema
180	1	2	Face value
180	2	2	Valor nominal / Apariencia
181	1	2	Fair-weather friend
181	2	2	Amigo de interés
182	1	2	Falling on deaf ears
182	2	2	Caer en saco roto
183	1	2	Few and far between
183	2	2	Raro / Escaso
184	1	2	Fighting a losing battle
184	2	2	Luchar una batalla perdida
185	1	2	Fit as a fiddle
185	2	2	Sano como una manzana
186	1	2	Flash in the pan
186	2	2	Flor de un día / Éxito pasajero
187	1	2	Fly on the wall
187	2	2	Testigo invisible
188	1	2	Follow in someone’s footsteps
188	2	2	Seguir los pasos de alguien
189	1	2	Food for thought
189	2	2	Algo para reflexionar
190	1	2	From rags to riches
190	2	2	De la miseria a la riqueza
191	1	2	Full of beans
191	2	2	Lleno de energía
192	1	2	Get wind of something
192	2	2	Enterarse de algo
193	1	2	Go Dutch
193	2	2	Pagar a medias
194	1	2	Grin and bear it
194	2	2	Al mal tiempo, buena cara
195	1	2	Hard nut to crack
195	2	2	Hueso duro de roer
196	1	2	Have your cake and eat it
196	2	2	Tenerlo todo / No poder estar en misa y repicando
197	1	2	Heart in your mouth
197	2	2	Con el corazón en un puño
198	1	2	High on the hog
198	2	2	Vivir por todo lo alto
199	1	2	Hold your horses
1	1	1	Piece of cake
1	2	1	Pan comido
2	1	1	Break a leg
2	2	1	Buena suerte / Romperse una pierna
3	1	1	Under the weather
3	2	1	Sentirse mal / Estar pachucho
4	1	1	Spill the beans
4	2	1	Soltar la lengua / Contar el secreto
5	1	1	Once in a blue moon
5	2	1	De higos a brevas / Muy rara vez
6	1	1	Cost an arm and a leg
6	2	1	Costar un ojo de la cara
7	1	1	Let the cat out of the bag
7	2	1	Descubrir el pastel
8	1	1	When pigs fly
8	2	1	Cuando las ranas críen pelo
9	1	1	Beat around the bush
9	2	1	Andarse con rodeos
10	1	1	Bite off more than you can chew
10	2	1	Quien mucho abarca poco aprieta
11	1	1	Barking up the wrong tree
11	2	1	Llamar a la puerta equivocada
12	1	1	Better late than never
12	2	1	Más vale tarde que nunca
13	1	1	Bite the bullet
13	2	1	Hacer de tripas corazón / Aguantar el tipo
14	1	1	Break the ice
14	2	1	Romper el hielo
15	1	1	By the skin of your teeth
15	2	1	Por los pelos
16	1	1	Don’t cry over spilled milk
16	2	1	A lo hecho, pecho
17	1	1	Every cloud has a silver lining
17	2	1	No hay mal que por bien no venga
18	1	1	Get a taste of your own medicine
18	2	1	Probar de su propia medicina
19	1	1	Give someone the cold shoulder
19	2	1	Hacer el vacío a alguien
20	1	1	Go the extra mile
20	2	1	Esforzarse al máximo
21	1	1	Hit the nail on the head
21	2	1	Dar en el clavo
22	1	1	Ignorance is bliss
22	2	1	La ignorancia da la felicidad
199	2	2	Para el carro / Calma
200	1	2	In the long run
200	2	2	A la larga
23	1	1	It takes two to tango
23	2	1	Dos no riñen si uno no quiere
24	1	1	Keep someone at bay
24	2	1	Mantener a raya
25	1	1	Kill two birds with one stone
25	2	1	Matar dos pájaros de un tiro
26	1	1	Last straw
26	2	1	La gota que colmó el vaso
27	1	1	Let sleeping dogs lie
27	2	1	Mejor no menearlo
28	1	1	Make a long story short
28	2	1	Para no alargarlo más
29	1	1	Miss the boat
29	2	1	Perder el tren / Oportunidad
30	1	1	No pain, no gain
30	2	1	Quien algo quiere, algo le cuesta
31	1	1	On the ball
31	2	1	Estar al tanto / Estar en lo que hay que estar
32	1	1	Pull someone’s leg
32	2	1	Tomar el pelo
33	1	1	Pull yourself together
33	2	1	Cálmate / Serénate
34	1	1	Sit on the fence
34	2	1	No mojarse / Estar indeciso
35	1	1	Speak of the devil
35	2	1	Hablando del rey de Roma
36	1	1	Take it with a grain of salt
36	2	1	Tomarlo con pinzas
37	1	1	The best of both worlds
37	2	1	Lo mejor de ambos mundos
38	1	1	Through thick and thin
38	2	1	A las duras y a las maduras
39	1	1	To make matters worse
39	2	1	Para colmo de males
40	1	1	Under the table
40	2	1	Bajo cuerda / Dinero negro
41	1	1	Up in the air
41	2	1	Estar en el aire
42	1	1	Wrap your head around something
42	2	1	Entender algo complejo
43	1	1	You can’t judge a book by its cover
43	2	1	Las apariencias engañan
44	1	1	A blessing in disguise
44	2	1	No hay mal que por bien no venga
45	1	1	A dime a dozen
45	2	1	Algo muy común / A patadas
46	1	1	Add insult to injury
46	2	1	Echar sal a la herida
47	1	1	Beat the clock
47	2	1	Hacer algo contra reloj
48	1	1	Bite your tongue
48	2	1	Morderse la lengua
49	1	1	Call it a day
49	2	1	Dar algo por terminado
50	1	1	Cut corners
50	2	1	Escatimar / Ir por el camino fácil
51	1	1	Cut someone some slack
51	2	1	Dar un margen a alguien
52	1	1	Easy does it
52	2	1	Con cuidado / Despacio
53	1	1	Get out of hand
53	2	1	Irse de las manos
54	1	1	Get something out of your system
54	2	1	Desahogarse
55	1	1	Hang in there
55	2	1	Aguanta ahí / No te rindas
56	1	1	In a nutshell
56	2	1	En pocas palabras / En resumen
57	1	1	Jump the gun
57	2	1	Precipitarse
58	1	1	Keep your chin up
58	2	1	Mantener la cabeza alta
59	1	1	Let someone off the hook
59	2	1	Librar a alguien del castigo
60	1	1	Live and learn
60	2	1	Vivir para aprender
61	1	1	Look before you leap
61	2	1	Antes de hacer nada, piénsalo bien
62	1	1	Make ends meet
62	2	1	Llegar a fin de mes
63	1	1	No strings attached
63	2	1	Sin compromiso
64	1	1	On thin ice
64	2	1	Pisar terreno pantanoso
65	1	1	Out of the blue
65	2	1	De la nada / De repente
66	1	1	Play it by ear
66	2	1	Improvisar sobre la marcha
67	1	1	Rain on someone’s parade
67	2	1	Aguar la fiesta a alguien
68	1	1	Saving for a rainy day
68	2	1	Ahorrar para cuando vengan las vacas flacas
69	1	1	See eye to eye
69	2	1	Estar de acuerdo
70	1	1	Slow and steady wins the race
70	2	1	Vísteme despacio que tengo prisa
71	1	1	Spill the tea
71	2	1	Contar el chisme
72	1	1	Straight from the horse’s mouth
72	2	1	De buena fuente
73	1	1	Take it easy
73	2	1	Tómalo con calma
74	1	1	The elephant in the room
74	2	1	Un problema obvio que se ignora
75	1	1	The whole nine yards
75	2	1	Con todo / Hasta el final
76	1	1	To burn bridges
76	2	1	Quemar las naves
77	1	1	To cut a long story short
77	2	1	En resumen
78	1	1	To feel blue
78	2	1	Estar deprimido / Estar triste
79	1	1	To give it a shot
79	2	1	Intentarlo / Darle una oportunidad
80	1	1	To go cold turkey
80	2	1	Dejar algo de golpe
81	1	1	To hit the hay
81	2	1	Irse al sobre / Irse a dormir
82	1	1	To keep an eye on
82	2	1	Vigilar / Echar un ojo
83	1	1	To lose your touch
83	2	1	Perder la maña
84	1	1	To ring a bell
84	2	1	Sonar de algo
85	1	1	To stab someone in the back
85	2	1	Apuñalar por la espalda
86	1	1	To twist someone’s arm
86	2	1	Convencer a alguien / Forzar la mano
87	1	1	Up for grabs
87	2	1	Disponible para cualquiera
88	1	1	Your guess is as good as mine
88	2	1	Ni idea / Sé lo mismo que tú
89	1	1	A piece of the pie
89	2	1	Parte del pastel / Beneficio
90	1	1	Back to square one
90	2	1	Volver a empezar de cero
91	1	1	Bite the dust
91	2	1	Morder el polvo
92	1	1	Blow off steam
92	2	1	Desahogarse / Soltar vapor
93	1	1	Burn the midnight oil
93	2	1	Quemarse las pestañas / Trasnochar trabajando
94	1	1	Couch potato
94	2	1	Persona sedentaria / Teleadicto
95	1	1	Don’t put all your eggs in one basket
95	2	1	No te lo juegues todo a una carta
96	1	1	Face the music
96	2	1	Dar la cara / Afrontar las consecuencias
97	1	1	Get cold feet
97	2	1	Echarse atrás / Tener miedo
98	1	1	Head over heels
98	2	1	Estar coladito por alguien
99	1	1	In the heat of the moment
99	2	1	En el fragor del momento
100	1	1	Look on the bright side
100	2	1	Ver el lado positivo
201	1	3	A penny for your thoughts
201	2	3	¿En qué estás pensando?
202	1	3	Barking up the wrong tree
202	2	3	Equivocar el camino / Errar el tiro
203	1	3	Beat a dead horse
203	2	3	Perder el tiempo en algo inútil
204	1	3	Bite the bullet
204	2	3	Aceptar una situación difícil con valor
205	1	3	Burn the midnight oil
205	2	3	Trabajar hasta muy tarde
206	1	3	Cry over spilled milk
206	2	3	Lamentarse por lo que ya no tiene remedio
207	1	3	Curiosity killed the cat
207	2	3	La curiosidad mató al gato
208	1	3	Don’t count your chickens before they hatch
208	2	3	No cantes victoria antes de tiempo
209	1	3	Every cloud has a silver lining
209	2	3	No hay mal que por bien no venga
210	1	3	Fit as a fiddle
210	2	3	Sano como una manzana
211	1	3	Go down in flames
211	2	3	Fracasar estrepitosamente
212	1	3	He has bigger fish to fry
212	2	3	Tiene asuntos más importantes que atender
213	1	3	Hear it on the grapevine
213	2	3	Enterarse por rumores
214	1	3	In for a penny, in for a pound
214	2	3	Perdido al río / Si empiezas algo, termínalo
215	1	3	It’s a long shot
215	2	3	Es poco probable
216	1	3	Keep your chin up
216	2	3	Mantener el ánimo alto
217	1	3	Kill two birds with one stone
217	2	3	Matar dos pájaros de un tiro
218	1	3	Let sleeping dogs lie
218	2	3	Mejor no revolver el asunto
219	1	3	Make a long story short
219	2	3	En resumidas cuentas
220	1	3	Method to my madness
220	2	3	Tener un plan pese a parecer loco
221	1	3	Miss the boat
221	2	3	Perder la oportunidad
222	1	3	Not a spark of decency
222	2	3	No tener ni pizca de decencia
223	1	3	Off the hook
223	2	3	Fuera de peligro / Librarse de una
224	1	3	On the ball
224	2	3	Estar en lo que hay que estar
225	1	3	Once in a blue moon
225	2	3	Muy de vez en cuando
226	1	3	Picture is worth a thousand words
226	2	3	Una imagen vale más que mil palabras
227	1	3	Piece of cake
227	2	3	Algo muy fácil
228	1	3	Pull someone’s leg
228	2	3	Tomar el pelo a alguien
229	1	3	Pull yourself together
229	2	3	Recupérate / Contrólate
230	1	3	See eye to eye
230	2	3	Estar de acuerdo
231	1	3	Sit on the fence
231	2	3	No decidirse / Estar en duda
232	1	3	Speak of the devil
232	2	3	Hablando del rey de Roma
233	1	3	Steal someone’s thunder
233	2	3	Quitarle el protagonismo a alguien
234	1	3	Take it with a grain of salt
234	2	3	No tomárselo al pie de la letra
235	1	3	Taste of your own medicine
235	2	3	Probar tu propia medicina
236	1	3	The best of both worlds
236	2	3	Lo mejor de dos situaciones
237	1	3	The elephant in the room
237	2	3	Un problema obvio que nadie quiere mencionar
238	1	3	The whole nine yards
238	2	3	Hasta el final / Con todo
239	1	3	Through thick and thin
239	2	3	En las buenas y en las malas
240	1	3	To add fuel to the fire
240	2	3	Echar leña al fuego
241	1	3	To bend over backwards
241	2	3	Hacer lo imposible por ayudar
242	1	3	To bite off more than you can chew
242	2	3	Abarcar más de lo que se puede
243	1	3	To cut corners
243	2	3	Ahorrar tiempo o dinero malamente
244	1	3	To feel under the weather
244	2	3	Sentirse un poco enfermo
245	1	3	To get out of hand
245	2	3	Irse de las manos
246	1	3	To hit the nail on the head
246	2	3	Dar en el clavo
247	1	3	To let the cat out of the bag
247	2	3	Revelar un secreto
248	1	3	To make matters worse
248	2	3	Para colmo de males
249	1	3	To miss the boat
249	2	3	Perder el tren / Oportunidad
250	1	3	To play devil’s advocate
250	2	3	Hacer de abogado del diablo
251	1	3	To pull the wool over someone’s eyes
251	2	3	Engañar a alguien / Dar gato por liebre
252	1	3	To see eye to eye
252	2	3	Coincidir en opinión
253	1	3	To sit on the fence
253	2	3	No tomar partido
254	1	3	To spill the beans
254	2	3	Cantar / Soltar el secreto
255	1	3	To take the bull by the horns
255	2	3	Afrontar el problema directamente
256	1	3	To throw caution to the wind
256	2	3	Arriesgarse sin miedo
257	1	3	To turn a blind eye
257	2	3	Hacer la vista gorda
258	1	3	Under the weather
258	2	3	Sentirse mal físicamente
259	1	3	Up in the air
259	2	3	Estar en el aire / Sin decidir
260	1	3	Wrap your head around something
260	2	3	Llegar a comprender algo difícil
261	1	3	You can’t judge a book by its cover
261	2	3	No juzgar por las apariencias
262	1	3	Your guess is as good as mine
262	2	3	Sé lo mismo que tú / Ni idea
263	1	3	A chip on your shoulder
263	2	3	Estar resentido por algo del pasado
264	1	3	A drop in the bucket
264	2	3	Una gota en el océano
265	1	3	A fool and his money are soon parted
265	2	3	A los tontos les dura poco el dinero
266	1	3	A golden handshake
266	2	3	Una jubilación dorada / Indemnización alta
267	1	3	A loose cannon
267	2	3	Una persona impredecible y peligrosa
268	1	3	A penny saved is a penny earned
268	2	3	Un centavo ahorrado es un centavo ganado
269	1	3	A piece of the action
269	2	3	Una parte del pastel / Beneficio
270	1	3	A sight for sore eyes
270	2	3	Una alegría para la vista
271	1	3	Actions speak louder than words
271	2	3	Las acciones valen más que las palabras
272	1	3	All in good time
272	2	3	Todo a su debido tiempo
273	1	3	Apple of my eye
273	2	3	La niña de mis ojos
274	1	3	As cool as a cucumber
274	2	3	Tranquilo como una lechuga
275	1	3	At the drop of a hat
275	2	3	A la primera de cambio / Sin dudar
276	1	3	Back to basics
276	2	3	Volver a lo fundamental
277	1	3	Barking dogs seldom bite
277	2	3	Perro que ladra no muerde
278	1	3	Beat around the bush
278	2	3	Andarse con rodeos
279	1	3	Beggars can’t be choosers
279	2	3	A falta de pan, buenas son tortas
280	1	3	Best thing since sliced bread
280	2	3	Lo mejor del mundo
281	1	3	Better safe than sorry
281	2	3	Más vale prevenir que lamentar
282	1	3	Between the devil and the deep blue sea
282	2	3	Entre la espada y la pared
283	1	3	Birds of a feather flock together
283	2	3	Dios los cría y ellos se juntan
284	1	3	Bite your tongue
284	2	3	Morderse la lengua
285	1	3	Blind leading the blind
285	2	3	Un ciego guiando a otro ciego
286	1	3	Blood is thicker than water
286	2	3	La sangre tira más que el agua
287	1	3	Break the ice
287	2	3	Romper el hielo
288	1	3	By the skin of your teeth
288	2	3	Por los pelos
289	1	3	Call it a day
289	2	3	Dar algo por terminado
290	1	3	Cat’s got your tongue?
290	2	3	¿Te ha comido la lengua el gato?
291	1	3	Caught between two stools
291	2	3	Indeciso entre dos opciones
292	1	3	Chew the fat
292	2	3	Charlar o cotillear un rato
293	1	3	Clean as a whistle
293	2	3	Limpio como una patena
294	1	3	Close but no cigar
294	2	3	Cerca, pero no lo suficiente
295	1	3	Come hell or high water
295	2	3	Contra viento y marea
296	1	3	Cross that bridge when you come to it
296	2	3	Cada día tiene su afán
297	1	3	Cut to the chase
297	2	3	Ir al grano
298	1	3	Dark horse
298	2	3	Candidato inesperado
299	1	3	Dead as a doornail
299	2	3	Más muerto que mi abuela
300	1	3	Devil’s advocate
300	2	3	Abogado del diablo
\.


--
-- TOC entry 5115 (class 0 OID 16734)
-- Dependencies: 222
-- Data for Name: nivel; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.nivel (id_nivel, nivel) FROM stdin;
1	Básico
2	Intermedio
3	Avanzado
\.


--
-- TOC entry 5125 (class 0 OID 24581)
-- Dependencies: 232
-- Data for Name: paises; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.paises (id_pais, pais) FROM stdin;
1	Argentina
2	Brasil
3	México
4	Estados Unidos
5	Canadá
6	España
7	Francia
8	Italia
9	Alemania
10	Argentina
11	Venezuela
12	Peru
13	Colombia
14	Argentina
15	Uruguay
16	Paraguay
17	Chile
18	Reino Unido
\.


--
-- TOC entry 5126 (class 0 OID 24604)
-- Dependencies: 233
-- Data for Name: palabras; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.palabras (id_palabra, id_lenguaje, id_tipo_palabra, id_nivel, palabra, subtipo) FROM stdin;
1743	2	5	1	Lograr	1
1743	1	5	1	Achieve	1
1744	2	5	1	Logró	2
1744	1	5	1	Achieved	2
1745	2	5	1	Logrado	3
1745	1	5	1	Achieved	3
1746	2	5	1	Admitir	1
1746	1	5	1	Admit	1
1747	2	5	1	Admitió	2
1747	1	5	1	Admitted	2
1748	2	5	1	Admitido	3
1748	1	5	1	Admitted	3
1749	2	5	1	Evitar	1
1749	1	5	1	Avoid	1
1750	2	5	1	Evitó	2
1750	1	5	1	Avoided	2
1751	2	5	1	Evitado	3
1751	1	5	1	Avoided	3
1752	2	5	1	Hornear	1
1752	1	5	1	Bake	1
1753	2	5	1	Horneó	2
1753	1	5	1	Baked	2
1754	2	5	1	Horneado	3
1754	1	5	1	Baked	3
1755	2	5	1	Culpar	1
1755	1	5	1	Blame	1
1756	2	5	1	Culpó	2
1756	1	5	1	Blamed	2
1757	2	5	1	Culpado	3
1757	1	5	1	Blamed	3
1758	2	5	1	Tomar prestado	1
1758	1	5	1	Borrow	1
1759	2	5	1	Tomó prestado	2
1759	1	5	1	Borrowed	2
1760	2	5	1	Tomado prestado	3
1760	1	5	1	Borrowed	3
1761	2	5	1	Causar	1
1761	1	5	1	Cause	1
1762	2	5	1	Causó	2
1762	1	5	1	Caused	2
1763	2	5	1	Causado	3
1763	1	5	1	Caused	3
1764	2	5	1	Reclamar	1
1764	1	5	1	Claim	1
1765	2	5	1	Reclamó	2
1765	1	5	1	Claimed	2
1766	2	5	1	Reclamado	3
1766	1	5	1	Claimed	3
1767	2	5	1	Comparar	1
1767	1	5	1	Compare	1
1768	2	5	1	Comparó	2
1768	1	5	1	Compared	2
1769	2	5	1	Comparado	3
1769	1	5	1	Compared	3
1770	2	5	1	Consistir	1
1770	1	5	1	Consist	1
1771	2	5	1	Consistió	2
1771	1	5	1	Consisted	2
1772	2	5	1	Consistido	3
1772	1	5	1	Consisted	3
1545	1	5	1	Accept	1
1545	2	5	1	Aceptar	1
1546	1	5	1	Accepted	2
1546	2	5	1	Aceptó / Aceptaba	2
1547	1	5	1	Accepted	3
1547	2	5	1	Aceptado	3
1548	1	5	1	Ask	1
1548	2	5	1	Preguntar	1
1549	1	5	1	Asked	2
1549	2	5	1	Preguntó / Preguntaba	2
1550	1	5	1	Asked	3
1550	2	5	1	Preguntado	3
1551	1	5	1	Call	1
1551	2	5	1	Llamar	1
1552	1	5	1	Called	2
1552	2	5	1	Llamó / Llamaba	2
1553	1	5	1	Called	3
1553	2	5	1	Llamado	3
1554	1	5	1	Clean	1
1554	2	5	1	Limpiar	1
1555	1	5	1	Cleaned	2
1555	2	5	1	Limpió / Limpiaba	2
1556	1	5	1	Cleaned	3
1556	2	5	1	Limpiado	3
1557	1	5	1	Cook	1
1557	2	5	1	Cocinar	1
1558	1	5	1	Cooked	2
1558	2	5	1	Cocinó / Cocinaba	2
1559	1	5	1	Cooked	3
1559	2	5	1	Cocinado	3
1773	2	10	1	Congelar	1
1773	1	10	1	Freeze	1
1774	2	10	1	Congeló	2
1774	1	10	1	Froze	2
1775	2	10	1	Congelado	3
1775	1	10	1	Frozen	3
1776	2	10	1	Esconder	1
1776	1	10	1	Hide	1
1777	2	10	1	Escondió	2
1777	1	10	1	Hid	2
1778	2	10	1	Escondido	3
1778	1	10	1	Hidden	3
1779	2	10	1	Montar	1
1779	1	10	1	Ride	1
1780	2	10	1	Montó	2
1780	1	10	1	Rode	2
1781	2	10	1	Montado	3
1781	1	10	1	Ridden	3
1782	2	10	1	Sacudir	1
1782	1	10	1	Shake	1
1783	2	10	1	Sacudió	2
1783	1	10	1	Shook	2
1784	2	10	1	Sacudido	3
1784	1	10	1	Shaken	3
1785	2	10	1	Gastar	1
1785	1	10	1	Spend	1
1786	2	10	1	Gastó	2
1786	1	10	1	Spent	2
1787	2	10	1	Gastado	3
1787	1	10	1	Spent	3
1788	2	10	1	Prestar	1
1788	1	10	1	Lend	1
1789	2	10	1	Prestó	2
1789	1	10	1	Lent	2
1790	2	10	1	Prestado	3
1790	1	10	1	Lent	3
1791	2	10	1	Surgir	1
1791	1	10	1	Arise	1
1792	2	10	1	Surgió	2
1792	1	10	1	Arose	2
1793	2	10	1	Surgido	3
1793	1	10	1	Arisen	3
1794	2	10	1	Soportar	1
1794	1	10	1	Bear	1
1795	2	10	1	Soportó	2
1560	1	5	1	Dance	1
1560	2	5	1	Bailar	1
1561	1	5	1	Danced	2
1561	2	5	1	Bailó / Bailaba	2
1562	1	5	1	Danced	3
1562	2	5	1	Bailado	3
1563	1	5	1	Enjoy	1
1563	2	5	1	Disfrutar	1
1564	1	5	1	Enjoyed	2
1564	2	5	1	Disfrutó / Disfrutaba	2
1565	1	5	1	Enjoyed	3
1565	2	5	1	Disfrutado	3
1566	1	5	1	Explain	1
1566	2	5	1	Explicar	1
1567	1	5	1	Explained	2
1567	2	5	1	Explicó / Explicaba	2
1568	1	5	1	Explained	3
1568	2	5	1	Explicado	3
1569	1	5	1	Finish	1
1569	2	5	1	Terminar	1
1570	1	5	1	Finished	2
1570	2	5	1	Terminó / Terminaba	2
1571	1	5	1	Finished	3
1571	2	5	1	Terminado	3
1572	1	5	1	Help	1
1572	2	5	1	Ayudar	1
1795	1	10	1	Bore	2
1796	2	10	1	Soportado	3
1796	1	10	1	Borne	3
1797	2	10	1	Doblar	1
1797	1	10	1	Bend	1
1798	2	10	1	Dobló	2
1798	1	10	1	Bent	2
1799	2	10	1	Doblado	3
1799	1	10	1	Bent	3
1800	2	10	1	Apostar	1
1800	1	10	1	Bet	1
1801	2	10	1	Apostó	2
1801	1	10	1	Bet	2
1802	2	10	1	Apostado	3
1802	1	10	1	Bet	3
1803	2	10	1	Atar	1
1803	1	10	1	Bind	1
1804	2	10	1	Ató	2
1804	1	10	1	Bound	2
1805	2	10	1	Atado	3
1805	1	10	1	Bound	3
1806	2	10	1	Sangrar	1
1806	1	10	1	Bleed	1
1807	2	10	1	Sangró	2
1807	1	10	1	Bled	2
1808	2	10	1	Sangrado	3
1808	1	10	1	Bled	3
1809	2	10	1	Criar	1
1809	1	10	1	Breed	1
1810	2	10	1	Crió	2
1810	1	10	1	Bred	2
1811	2	10	1	Criado	3
1811	1	10	1	Bred	3
1812	2	10	1	Tratar	1
1812	1	10	1	Deal	1
1813	2	10	1	Trató	2
1813	1	10	1	Dealt	2
1814	2	10	1	Tratado	3
1814	1	10	1	Dealt	3
1815	2	10	1	Cavar	1
1815	1	10	1	Dig	1
1816	2	10	1	Cavó	2
1816	1	10	1	Dug	2
1817	2	10	1	Cavado	3
1817	1	10	1	Dug	3
1818	2	10	1	Alimentar	1
1818	1	10	1	Feed	1
1819	2	10	1	Alimentó	2
1819	1	10	1	Fed	2
1820	2	10	1	Alimentado	3
1820	1	10	1	Fed	3
1821	2	10	1	Perdonar	1
1821	1	10	1	Forgive	1
1822	2	10	1	Perdonó	2
1822	1	10	1	Forgave	2
1823	2	10	1	Perdonado	3
1823	1	10	1	Forgiven	3
1824	2	10	1	Arrodillarse	1
1824	1	10	1	Kneel	1
1573	1	5	1	Helped	2
1573	2	5	1	Ayudó / Ayudaba	2
1574	1	5	1	Helped	3
1574	2	5	1	Ayudado	3
1575	1	5	1	Jump	1
1575	2	5	1	Saltar	1
1576	1	5	1	Jumped	2
1576	2	5	1	Saltó / Saltaba	2
1577	1	5	1	Jumped	3
1577	2	5	1	Saltado	3
1578	1	5	1	Like	1
1578	2	5	1	Gustar	1
1579	1	5	1	Liked	2
1579	2	5	1	Gustó / Gustaba	2
1580	1	5	1	Liked	3
1580	2	5	1	Gustado	3
1581	1	5	1	Listen	1
1581	2	5	1	Escuchar	1
1582	1	5	1	Listened	2
1582	2	5	1	Escuchó / Escuchaba	2
1583	1	5	1	Listened	3
1583	2	5	1	Escuchado	3
1584	1	5	1	Live	1
1584	2	5	1	Vivir	1
187	1	1	1	End	1
1825	2	10	1	Se arrodilló	2
1825	1	10	1	Knelt	2
1826	2	10	1	Arrodillado	3
1826	1	10	1	Knelt	3
1827	2	10	1	Guiar	1
1827	1	10	1	Lead	1
1828	2	10	1	Guió	2
1828	1	10	1	Led	2
1829	2	10	1	Guiado	3
1829	1	10	1	Led	3
1830	2	10	1	Significar	1
1830	1	10	1	Mean	1
1831	2	10	1	Significó	2
1831	1	10	1	Meant	2
1832	2	10	1	Significado	3
1832	1	10	1	Meant	3
1833	2	10	1	Buscar	1
1833	1	10	1	Seek	1
1834	2	10	1	Buscó	2
1834	1	10	1	Sought	2
1835	2	10	1	Buscado	3
1835	1	10	1	Sought	3
1836	2	10	1	Encoger	1
1836	1	10	1	Shrink	1
1837	2	10	1	Encogió	2
1837	1	10	1	Shrank	2
1838	2	10	1	Encogido	3
1838	1	10	1	Shrunk	3
1839	2	10	1	Deslizar	1
1839	1	10	1	Slide	1
1840	2	10	1	Deslizó	2
1840	1	10	1	Slid	2
1841	2	10	1	Deslizado	3
1841	1	10	1	Slid	3
1842	2	10	1	Escupit	1
1842	1	10	1	Spit	1
1843	2	10	1	Escupió	2
1843	1	10	1	Spat	2
1844	2	10	1	Escupido	3
1844	1	10	1	Spat	3
1845	2	10	1	Estropear	1
1845	1	10	1	Spoil	1
1846	2	10	1	Estropeó	2
1846	1	10	1	Spoiled	2
1847	2	10	1	Estropeado	3
1847	1	10	1	Spoiled	3
1848	2	10	1	Extender	1
1848	1	10	1	Spread	1
1849	2	10	1	Extendió	2
1849	1	10	1	Spread	2
1850	2	10	1	Extendido	3
1850	1	10	1	Spread	3
1851	2	10	1	Jurar	1
1851	1	10	1	Swear	1
1852	2	10	1	Juró	2
1852	1	10	1	Swore	2
1853	2	10	1	Jurado	3
1853	1	10	1	Sworn	3
1585	1	5	1	Lived	2
1585	2	5	1	Vivió / Vivía	2
1586	1	5	1	Lived	3
1586	2	5	1	Vivido	3
1587	1	5	1	Look	1
1587	2	5	1	Mirar	1
1588	1	5	1	Looked	2
1588	2	5	1	Miró / Miraba	2
1589	1	5	1	Looked	3
1589	2	5	1	Mirado	3
1590	1	5	1	Need	1
1590	2	5	1	Necesitar	1
1591	1	5	1	Needed	2
1591	2	5	1	Necesitó / Necesitaba	2
1592	1	5	1	Needed	3
1592	2	5	1	Necesitado	3
1593	1	5	1	Open	1
1593	2	5	1	Abrir	1
1594	1	5	1	Opened	2
1594	2	5	1	Abrió / Abría	2
1595	1	5	1	Opened	3
1595	2	5	1	Abierto	3
1596	1	5	1	Paint	1
1596	2	5	1	Pintar	1
1597	1	5	1	Painted	2
1597	2	5	1	Pintó / Pintaba	2
1598	1	5	1	Painted	3
1598	2	5	1	Pintado	3
1599	1	5	1	Play	1
1599	2	5	1	Jugar	1
1600	1	5	1	Played	2
1600	2	5	1	Jugó / Jugaba	2
1601	1	5	1	Played	3
1601	2	5	1	Jugado	3
1854	2	5	1	Rastrear	1
1854	1	5	1	Trace	1
1855	2	5	1	Rastreó	2
1855	1	5	1	Traced	2
1856	2	5	1	Rastreado	3
1856	1	5	1	Traced	3
1857	2	5	1	Girar	1
1857	1	5	1	Turn	1
1858	2	5	1	Giró	2
1858	1	5	1	Turned	2
1859	2	5	1	Girado	3
1859	1	5	1	Turned	3
1860	2	5	1	Variar	1
1860	1	5	1	Vary	1
1861	2	5	1	Varió	2
1861	1	5	1	Varied	2
1862	2	5	1	Variado	3
1862	1	5	1	Varied	3
1863	2	5	1	Desear	1
1863	1	5	1	Wish	1
1864	2	5	1	Deseó	2
1864	1	5	1	Wished	2
1865	2	5	1	Deseado	3
1865	1	5	1	Wished	3
1866	2	5	1	Gritar	1
1866	1	5	1	Yell	1
1867	2	5	1	Gritó	2
1867	1	5	1	Yelled	2
1868	2	5	1	Gritado	3
1868	1	5	1	Yelled	3
2910	1	5	3	Neutralize	1
2911	2	5	3	Neutralizar	1
2912	1	5	3	Neutralized	2
2913	2	5	3	Neutralizó	2
2914	1	5	3	Neutralized	3
2915	2	5	3	Neutralizado	3
2916	1	5	3	Originate	1
2917	2	5	3	Originar	1
2918	1	5	3	Originated	2
2919	2	5	3	Originó	2
2920	1	5	3	Originated	3
2921	2	5	3	Originado	3
2922	1	5	3	Overcome	1
2923	2	5	3	Superar	1
2924	1	5	3	Overcomed	2
2925	2	5	3	Superó	2
2926	1	5	3	Overcomed	3
2927	2	5	3	Superado	3
2928	1	5	3	Participate	1
2929	2	5	3	Participar	1
2930	1	5	3	Participated	2
2931	2	5	3	Participó	2
2932	1	5	3	Participated	3
2933	2	5	3	Participado	3
2934	1	5	3	Persevere	1
2935	2	5	3	Perseverar	1
2936	1	5	3	Persevered	2
1602	1	5	1	Push	1
1602	2	5	1	Empujar	1
1603	1	5	1	Pushed	2
1603	2	5	1	Empujó / Empujaba	2
1604	1	5	1	Pushed	3
1604	2	5	1	Empujado	3
1605	1	5	1	Rain	1
1605	2	5	1	Llover	1
1606	1	5	1	Rained	2
1606	2	5	1	Llovió / Llovía	2
1607	1	5	1	Rained	3
1607	2	5	1	Llovido	3
1608	1	5	1	Remember	1
1608	2	5	1	Recordar	1
1609	1	5	1	Remembered	2
1609	2	5	1	Recordó / Recordaba	2
1610	1	5	1	Remembered	3
1610	2	5	1	Recordado	3
1611	1	5	1	Show	1
1611	2	5	1	Mostrar	1
1612	1	5	1	Showed	2
1612	2	5	1	Mostró / Mostraba	2
1613	1	5	1	Showed	3
1613	2	5	1	Mostrado	3
1614	1	5	1	Start	1
1614	2	5	1	Comenzar	1
2937	2	5	3	Perseveró	2
2938	1	5	3	Persevered	3
2939	2	5	3	Perseverado	3
2940	1	5	3	Rationalize	1
2941	2	5	3	Racionalizar	1
2942	1	5	3	Rationalized	2
2943	2	5	3	Racionalizó	2
2944	1	5	3	Rationalized	3
2945	2	5	3	Racionalizado	3
2946	1	5	3	Reconcile	1
2947	2	5	3	Reconciliar	1
2948	1	5	3	Reconciled	2
2949	2	5	3	Reconcilió	2
2950	1	5	3	Reconciled	3
2951	2	5	3	Reconciliado	3
2952	1	5	3	Reconstruct	1
2953	2	5	3	Reconstruir	1
2954	1	5	3	Reconstructed	2
2955	2	5	3	Reconstruyó	2
2956	1	5	3	Reconstructed	3
2957	2	5	3	Reconstruido	3
2958	1	5	3	Regulate	1
2959	2	5	3	Regular	1
2960	1	5	3	Regulated	2
2961	2	5	3	Reguló	2
2962	1	5	3	Regulated	3
2963	2	5	3	Regulado	3
2964	1	5	3	Reiterate	1
2965	2	5	3	Reiterar	1
2966	1	5	3	Reiterated	2
2967	2	5	3	Reiteró	2
2968	1	5	3	Reiterated	3
2969	2	5	3	Reiterado	3
2970	1	5	3	Rejuvenate	1
2971	2	5	3	Rejuvenecer	1
2972	1	5	3	Rejuvenated	2
2973	2	5	3	Rejuveneció	2
2974	1	5	3	Rejuvenated	3
2975	2	5	3	Rejuvenecido	3
2976	1	5	3	Saturate	1
2977	2	5	3	Saturar	1
2978	1	5	3	Saturated	2
2979	2	5	3	Saturó	2
2980	1	5	3	Saturated	3
2981	2	5	3	Saturado	3
2982	1	5	3	Scrutinize	1
2983	2	5	3	Escrutar	1
2984	1	5	3	Scrutinized	2
2985	2	5	3	Escrutó	2
2986	1	5	3	Scrutinized	3
2987	2	5	3	Escrutado	3
2988	1	5	3	Simplify	1
2989	2	5	3	Simplificar	1
2990	1	5	3	Simplified	2
2991	2	5	3	Simplificó	2
2992	1	5	3	Simplified	3
2993	2	5	3	Simplificado	3
2994	1	5	3	Speculate	1
2995	2	5	3	Especular	1
2996	1	5	3	Speculated	2
2997	2	5	3	Especuló	2
2998	1	5	3	Speculated	3
2999	2	5	3	Especulado	3
3000	1	5	3	Substantiate	1
1615	1	5	1	Started	2
1615	2	5	1	Comenzó / Comenzaba	2
1616	1	5	1	Started	3
1616	2	5	1	Comenzado	3
1617	1	5	1	Stay	1
1617	2	5	1	Quedarse	1
1618	1	5	1	Stayed	2
1618	2	5	1	Quedó / Quedaba	2
1619	1	5	1	Stayed	3
1619	2	5	1	Quedado	3
1620	1	5	1	Study	1
1620	2	5	1	Estudiar	1
1621	1	5	1	Studied	2
1621	2	5	1	Estudió / Estudiaba	2
1622	1	5	1	Studied	3
1622	2	5	1	Estudiado	3
1623	1	5	1	Talk	1
1623	2	5	1	Hablar	1
1624	1	5	1	Talked	2
1624	2	5	1	Habló / Hablaba	2
1625	1	5	1	Talked	3
1625	2	5	1	Hablado	3
1626	1	5	1	Travel	1
1626	2	5	1	Viajar	1
1627	1	5	1	Traveled	2
1627	2	5	1	Viajó / Viajaba	2
1628	1	5	1	Traveled	3
1628	2	5	1	Viajado	3
1629	1	5	1	Use	1
1629	2	5	1	Usar	1
1630	1	5	1	Used	2
1630	2	5	1	Usó / Usaba	2
3001	2	5	3	Sustanciar	1
3002	1	5	3	Substantiated	2
3003	2	5	3	Sustanció	2
3004	1	5	3	Substantiated	3
3005	2	5	3	Sustanciado	3
3006	1	5	3	Synchronize	1
3007	2	5	3	Sincronizar	1
3008	1	5	3	Synchronized	2
3009	2	5	3	Sincronizó	2
3010	1	5	3	Synchronized	3
3011	2	5	3	Sincronizado	3
3012	1	5	3	Systematize	1
3013	2	5	3	Sistematizar	1
3014	1	5	3	Systematized	2
3015	2	5	3	Sistematizó	2
3016	1	5	3	Systematized	3
3017	2	5	3	Sistematizado	3
3018	1	5	3	Tolerate	1
3019	2	5	3	Tolerar	1
3020	1	5	3	Tolerated	2
3021	2	5	3	Toleró	2
3022	1	5	3	Tolerated	3
3023	2	5	3	Tolerado	3
3024	1	5	3	Transform	1
3025	2	5	3	Transformar	1
3026	1	5	3	Transformed	2
3027	2	5	3	Transformó	2
3028	1	5	3	Transformed	3
3029	2	5	3	Transformado	3
3030	1	5	3	Unify	1
3031	2	5	3	Unificar	1
3032	1	5	3	Unified	2
3033	2	5	3	Unificó	2
3034	1	5	3	Unified	3
3035	2	5	3	Unificado	3
3036	1	5	3	Validate	1
3037	2	5	3	Validar	1
3038	1	5	3	Validated	2
3039	2	5	3	Validó	2
3040	1	5	3	Validated	3
3041	2	5	3	Validado	3
3042	1	5	3	Verify	1
3043	2	5	3	Verificar	1
3044	1	5	3	Verified	2
3045	2	5	3	Verificó	2
3046	1	5	3	Verified	3
3047	2	5	3	Verificado	3
3048	1	5	3	Visualize	1
3049	2	5	3	Visualizar	1
3050	1	5	3	Visualized	2
3051	2	5	3	Visualizó	2
3052	1	5	3	Visualized	3
3053	2	5	3	Visualizado	3
3054	1	5	3	Withstand	1
3055	2	5	3	Resistir	1
3056	1	5	3	Withstood	2
3057	2	5	3	Resistió	2
3058	1	5	3	Withstood	3
3059	2	5	3	Resistido	3
3060	1	10	1	Become	1
3061	2	10	1	Convertirse	1
3062	1	10	1	Became	2
3063	2	10	1	Se convirtió	2
3064	1	10	1	Become	3
3065	2	10	1	Convertido	3
3066	1	10	1	Bite	1
3067	2	10	1	Morder	1
3068	1	10	1	Bit	2
3069	2	10	1	Mordió	2
3070	1	10	1	Bitten	3
3071	2	10	1	Mordido	3
3072	1	10	1	Bleed	1
3073	2	10	1	Sangrar	1
3074	1	10	1	Bled	2
3075	2	10	1	Sangró	2
3076	1	10	1	Bled	3
3077	2	10	1	Sangrado	3
3078	1	10	1	Blow	1
3079	2	10	1	Soplar	1
3080	1	10	1	Blew	2
3081	2	10	1	Sopló	2
3082	1	10	1	Blown	3
3083	2	10	1	Soplado	3
3084	1	10	1	Choose	1
3085	2	10	1	Elegir	1
3086	1	10	1	Chose	2
3087	2	10	1	Eligió	2
3088	1	10	1	Chosen	3
3089	2	10	1	Elegido	3
3090	1	10	1	Deal	1
3091	2	10	1	Tratar	1
3092	1	10	1	Dealt	2
3093	2	10	1	Trató	2
3094	1	10	1	Dealt	3
3095	2	10	1	Tratado	3
3096	1	10	1	Dig	1
3097	2	10	1	Cavar	1
3098	1	10	1	Dug	2
3099	2	10	1	Cavó	2
3100	1	10	1	Dug	3
3101	2	10	1	Cavado	3
3102	1	10	1	Dream	1
3103	2	10	1	Soñar	1
3104	1	10	1	Dreamt	2
3105	2	10	1	Soñó	2
3106	1	10	1	Dreamt	3
3107	2	10	1	Soñado	3
3108	1	10	1	Feed	1
3109	2	10	1	Alimentar	1
3110	1	10	1	Fed	2
3111	2	10	1	Alimentó	2
3112	1	10	1	Fed	3
3113	2	10	1	Alimentado	3
3114	1	10	1	Fight	1
3115	2	10	1	Pelear	1
3116	1	10	1	Fought	2
3117	2	10	1	Peleó	2
3118	1	10	1	Fought	3
3119	2	10	1	Peleado	3
3120	1	10	1	Fit	1
3121	2	10	1	Quedar	1
3122	1	10	1	Fit	2
3123	2	10	1	Quedó	2
3124	1	10	1	Fit	3
3125	2	10	1	Quedado	3
3126	1	10	1	Freeze	1
3127	2	10	1	Congelar	1
3128	1	10	1	Froze	2
3129	2	10	1	Congeló	2
3130	1	10	1	Frozen	3
3131	2	10	1	Congelado	3
3132	1	10	1	Hang	1
3133	2	10	1	Colgar	1
3134	1	10	1	Hung	2
3135	2	10	1	Colgó	2
3136	1	10	1	Hung	3
3137	2	10	1	Colgado	3
3138	1	10	1	Hide	1
3139	2	10	1	Esconder	1
3140	1	10	1	Hid	2
3141	2	10	1	Escondió	2
3142	1	10	1	Hidden	3
3143	2	10	1	Escondido	3
3144	1	10	1	Hold	1
3145	2	10	1	Sostener	1
3146	1	10	1	Held	2
3147	2	10	1	Sostuvo	2
3148	1	10	1	Held	3
3149	2	10	1	Sostenido	3
3150	1	10	1	Hurt	1
3151	2	10	1	Herir	1
3152	1	10	1	Hurt	2
3153	2	10	1	Hirió	2
3154	1	10	1	Hurt	3
3155	2	10	1	Herido	3
3156	1	10	1	Lead	1
3157	2	10	1	Guiar	1
3158	1	10	1	Led	2
3159	2	10	1	Guió	2
3160	1	10	1	Led	3
3161	2	10	1	Guiado	3
3162	1	10	1	Lend	1
3163	2	10	1	Prestar	1
3164	1	10	1	Lent	2
3165	2	10	1	Prestó	2
3166	1	10	1	Lent	3
3167	2	10	1	Prestado	3
3168	1	10	1	Light	1
3169	2	10	1	Encender	1
3170	1	10	1	Lit	2
3171	2	10	1	Encendió	2
3172	1	10	1	Lit	3
3173	2	10	1	Encendido	3
3174	1	10	1	Mean	1
3175	2	10	1	Significar	1
3176	1	10	1	Meant	2
3177	2	10	1	Significó	2
3178	1	10	1	Meant	3
3179	2	10	1	Significado	3
3180	1	10	1	Quit	1
3181	2	10	1	Abandonar	1
3182	1	10	1	Quit	2
3183	2	10	1	Abandonó	2
3184	1	10	1	Quit	3
3185	2	10	1	Abandonado	3
3186	1	10	1	Rise	1
3187	2	10	1	Elevar	1
3188	1	10	1	Rose	2
3189	2	10	1	Elevó	2
3190	1	10	1	Risen	3
3191	2	10	1	Elevado	3
3192	1	10	1	Shake	1
3193	2	10	1	Sacudir	1
3194	1	10	1	Shook	2
3195	2	10	1	Sacudió	2
3196	1	10	1	Shaken	3
3197	2	10	1	Sacudido	3
3198	1	10	1	Shine	1
3199	2	10	1	Brillar	1
3200	1	10	1	Shone	2
3201	2	10	1	Brilló	2
3202	1	10	1	Shone	3
3203	2	10	1	Brillado	3
3204	1	10	1	Shoot	1
3205	2	10	1	Disparar	1
3206	1	10	1	Shot	2
3207	2	10	1	Disparó	2
3208	1	10	1	Shot	3
3209	2	10	1	Disparado	3
3210	1	10	1	Shut	1
3211	2	10	1	Cerrar	1
3212	1	10	1	Shut	2
3213	2	10	1	Cerró	2
3214	1	10	1	Shut	3
3215	2	10	1	Cerrado	3
3216	1	10	1	Sink	1
3217	2	10	1	Hundir	1
3218	1	10	1	Sank	2
3219	2	10	1	Hundió	2
3220	1	10	1	Sunk	3
3221	2	10	1	Hundido	3
2174	1	5	1	Locked	2
2175	2	5	1	Cerró	2
2176	1	5	1	Locked	3
2177	2	5	1	Cerrado	3
2178	1	5	1	Manage	1
2179	2	5	1	Gestionar	1
2180	1	5	1	Managed	2
2181	2	5	1	Gestionó	2
2182	1	5	1	Managed	3
2183	2	5	1	Gestionado	3
2184	1	5	1	Mark	1
2185	2	5	1	Marcar	1
2186	1	5	1	Marked	2
2187	2	5	1	Marcó	2
2188	1	5	1	Marked	3
2189	2	5	1	Marcado	3
2190	1	5	1	Notice	1
2191	2	5	1	Notar	1
2192	1	5	1	Noticed	2
2193	2	5	1	Notó	2
2194	1	5	1	Noticed	3
2195	2	5	1	Notado	3
2196	1	5	1	Order	1
2197	2	5	1	Ordenar	1
2198	1	5	1	Ordered	2
2199	2	5	1	Ordenó	2
2200	1	5	1	Ordered	3
2201	2	5	1	Ordenado	3
2202	1	5	1	Own	1
2203	2	5	1	Poseer	1
2204	1	5	1	Owned	2
2205	2	5	1	Poseyó	2
2206	1	5	1	Owned	3
2207	2	5	1	Poseído	3
2208	1	5	1	Pack	1
2209	2	5	1	Empacar	1
2210	1	5	1	Packed	2
2211	2	5	1	Empacó	2
2212	1	5	1	Packed	3
2213	2	5	1	Empacado	3
2214	1	5	1	Pass	1
2215	2	5	1	Pasar	1
2216	1	5	1	Passed	2
2217	2	5	1	Pasó	2
2218	1	5	1	Passed	3
2219	2	5	1	Pasado	3
2220	1	5	1	Perform	1
2221	2	5	1	Realizar	1
2222	1	5	1	Performed	2
2223	2	5	1	Realizó	2
2224	1	5	1	Performed	3
2225	2	5	1	Realizado	3
2226	1	5	1	Pick	1
2227	2	5	1	Recoger	1
2228	1	5	1	Picked	2
2229	2	5	1	Recogió	2
2230	1	5	1	Picked	3
2231	2	5	1	Recogido	3
2232	1	5	1	Point	1
2233	2	5	1	Señalar	1
2234	1	5	1	Pointed	2
2235	2	5	1	Señaló	2
2236	1	5	1	Pointed	3
2237	2	5	1	Señalado	3
2238	1	5	1	Realize	1
2239	2	5	1	Comprender	1
2240	1	5	1	Realized	2
2241	2	5	1	Comprendió	2
2242	1	5	1	Realized	3
2243	2	5	1	Comprendido	3
1869	1	10	1	Awake	1
1869	2	10	1	Despertar	1
1870	1	10	1	Awoke	2
1870	2	10	1	Despertó	2
1871	1	10	1	Awoken	3
1871	2	10	1	Despertado	3
1872	1	10	1	Blow	1
1872	2	10	1	Soplar	1
1873	1	10	1	Blew	2
1873	2	10	1	Sopló	2
1874	1	10	1	Blown	3
1874	2	10	1	Soplado	3
1875	1	10	1	Break	1
1875	2	10	1	Romper	1
1876	1	10	1	Broke	2
1876	2	10	1	Rompió	2
1877	1	10	1	Broken	3
1877	2	10	1	Roto	3
1878	1	10	1	Bring	1
1878	2	10	1	Traer	1
1879	1	10	1	Brought	2
1879	2	10	1	Trajo	2
1880	1	10	1	Brought	3
1880	2	10	1	Traído	3
1881	1	10	1	Build	1
1881	2	10	1	Construir	1
1882	1	10	1	Built	2
1882	2	10	1	Construyó	2
1883	1	10	1	Built	3
1883	2	10	1	Construido	3
1884	1	10	1	Burn	1
1884	2	10	1	Quemar	1
1885	1	10	1	Burnt	2
1885	2	10	1	Quemó	2
1886	1	10	1	Burnt	3
1886	2	10	1	Quemado	3
1887	1	10	1	Buy	1
1887	2	10	1	Comprar	1
1888	1	10	1	Bought	2
1631	1	5	1	Used	3
1631	2	5	1	Usado	3
1632	1	5	1	Wait	1
1632	2	5	1	Esperar	1
1633	1	5	1	Waited	2
1633	2	5	1	Esperó / Esperaba	2
1634	1	5	1	Waited	3
1634	2	5	1	Esperado	3
1635	1	5	1	Walk	1
1635	2	5	1	Caminar	1
1636	1	5	1	Walked	2
1636	2	5	1	Caminó / Caminaba	2
1637	1	5	1	Walked	3
1637	2	5	1	Caminado	3
1638	1	5	1	Want	1
1638	2	5	1	Querer	1
1639	1	5	1	Wanted	2
1639	2	5	1	Quiso / Quería	2
1640	1	5	1	Wanted	3
1640	2	5	1	Querido	3
1641	1	5	1	Work	1
1641	2	5	1	Trabajar	1
1642	1	5	1	Worked	2
1642	2	5	1	Trabajó / Trabajaba	2
1643	1	5	1	Worked	3
1643	2	5	1	Trabajado	3
1	1	1	1	Home	1
2	2	1	1	Hogar	1
3	1	1	1	Water	1
4	2	1	1	Agua	1
5	1	1	1	Friend	1
6	2	1	1	Amigo	1
7	1	1	1	Family	1
8	2	1	1	Familia	1
9	1	1	1	City	1
10	2	1	1	Ciudad	1
11	1	1	1	School	1
12	2	1	1	Escuela	1
13	1	1	1	Book	1
14	2	1	1	Libro	1
15	1	1	1	Time	1
16	2	1	1	Tiempo	1
17	1	1	1	World	1
18	2	1	1	Mundo	1
19	1	1	1	Life	1
20	2	1	1	Vida	1
21	1	1	1	Food	1
22	2	1	1	Comida	1
23	1	1	1	Sun	1
24	2	1	1	Sol	1
25	1	1	1	Moon	1
26	2	1	1	Luna	1
27	1	1	1	Tree	1
28	2	1	1	Árbol	1
29	1	1	1	Money	1
30	2	1	1	Dinero	1
31	1	2	1	Good	1
1888	2	10	1	Compró	2
1889	1	10	1	Bought	3
1889	2	10	1	Comprado	3
1890	1	10	1	Catch	1
1890	2	10	1	Atrapar	1
1891	1	10	1	Caught	2
1891	2	10	1	Atrapó	2
1892	1	10	1	Caught	3
1892	2	10	1	Atrapado	3
1893	1	10	1	Choose	1
1893	2	10	1	Elegir	1
1894	1	10	1	Chose	2
1894	2	10	1	Eligió	2
1895	1	10	1	Chosen	3
1895	2	10	1	Elegido	3
1896	1	10	1	Come	1
1896	2	10	1	Venir	1
1897	1	10	1	Came	2
1897	2	10	1	Vino	2
1898	1	10	1	Come	3
1898	2	10	1	Venido	3
1899	1	10	1	Cost	1
1899	2	10	1	Costar	1
1900	1	10	1	Cost	2
1900	2	10	1	Costó	2
1901	1	10	1	Cost	3
1901	2	10	1	Costado	3
1902	1	10	1	Draw	1
1902	2	10	1	Dibujar	1
1903	1	10	1	Drew	2
1903	2	10	1	Dibujó	2
1904	1	10	1	Drawn	3
1904	2	10	1	Dibujado	3
1905	1	10	1	Dream	1
1905	2	10	1	Soñar	1
1906	1	10	1	Dreamt	2
1906	2	10	1	Soñó	2
1907	1	10	1	Dreamt	3
1907	2	10	1	Soñado	3
1644	1	5	1	Answer	1
1644	2	5	1	Responder / Contestar	1
1645	1	5	1	Answered	2
1645	2	5	1	Respondió / Respondía	2
1646	1	5	1	Answered	3
1646	2	5	1	Respondido	3
1647	1	5	1	Arrive	1
1647	2	5	1	Llegar	1
1648	1	5	1	Arrived	2
1648	2	5	1	Llegó / Llegaba	2
1649	1	5	1	Arrived	3
1649	2	5	1	Llegado	3
1650	1	5	1	Belong	1
1650	2	5	1	Pertenecer	1
1651	1	5	1	Belonged	2
1651	2	5	1	Perteneció / Pertenecía	2
1652	1	5	1	Belonged	3
1652	2	5	1	Pertenecido	3
1653	1	5	1	Change	1
1653	2	5	1	Cambiar	1
1654	1	5	1	Changed	2
1654	2	5	1	Cambió / Cambiaba	2
1655	1	5	1	Changed	3
1655	2	5	1	Cambiado	3
1656	1	5	1	Close	1
1656	2	5	1	Cerrar	1
1657	1	5	1	Closed	2
1657	2	5	1	Cerró / Cerraba	2
1658	1	5	1	Closed	3
1658	2	5	1	Cerrado	3
1659	1	5	1	Count	1
1908	1	10	1	Drink	1
1908	2	10	1	Beber	1
1909	1	10	1	Drank	2
1909	2	10	1	Bebió	2
1910	1	10	1	Drunk	3
1910	2	10	1	Bebido	3
1911	1	10	1	Drive	1
1911	2	10	1	Conducir	1
1912	1	10	1	Drove	2
1912	2	10	1	Condujo	2
1913	1	10	1	Driven	3
1913	2	10	1	Conducido	3
1914	1	10	1	Eat	1
1914	2	10	1	Comer	1
1915	1	10	1	Ate	2
1915	2	10	1	Comió	2
1916	1	10	1	Eaten	3
1916	2	10	1	Comido	3
1917	1	10	1	Fall	1
1917	2	10	1	Caer	1
1918	1	10	1	Fell	2
1918	2	10	1	Cayó	2
1919	1	10	1	Fallen	3
1919	2	10	1	Caído	3
1920	1	10	1	Fight	1
1920	2	10	1	Pelear	1
1921	1	10	1	Fought	2
1921	2	10	1	Peleó	2
1922	1	10	1	Fought	3
1922	2	10	1	Peleado	3
1923	1	10	1	Find	1
1923	2	10	1	Encontrar	1
1924	1	10	1	Found	2
1924	2	10	1	Encontró	2
1925	1	10	1	Found	3
1925	2	10	1	Encontrado	3
1926	1	10	1	Fly	1
1926	2	10	1	Volar	1
1927	1	10	1	Flew	2
1927	2	10	1	Voló	2
1928	1	10	1	Flown	3
1928	2	10	1	Volado	3
1929	1	10	1	Forget	1
1929	2	10	1	Olvidar	1
1930	1	10	1	Forgot	2
1930	2	10	1	Olvidó	2
1931	1	10	1	Forgotten	3
1931	2	10	1	Olvidado	3
1932	1	10	1	Get	1
1932	2	10	1	Obtener	1
1933	1	10	1	Got	2
1933	2	10	1	Obtuvo	2
1934	1	10	1	Gotten	3
1934	2	10	1	Obtenido	3
1935	1	10	1	Give	1
1935	2	10	1	Dar	1
1936	1	10	1	Gave	2
1936	2	10	1	Dio	2
1937	1	10	1	Given	3
1937	2	10	1	Dado	3
1938	1	10	1	Go	1
1938	2	10	1	Ir	1
1939	1	10	1	Went	2
1939	2	10	1	Fue	2
1940	1	10	1	Gone	3
1940	2	10	1	Ido	3
1941	1	10	1	Grow	1
1941	2	10	1	Crecer	1
1942	1	10	1	Grew	2
1942	2	10	1	Creció	2
1943	1	10	1	Grown	3
1943	2	10	1	Crecido	3
1944	1	10	1	Hang	1
1944	2	10	1	Colgar	1
1945	1	10	1	Hung	2
1945	2	10	1	Colgó	2
1946	1	10	1	Hung	3
1946	2	10	1	Colgado	3
1947	1	10	1	Have	1
1947	2	10	1	Tener	1
1948	1	10	1	Had	2
1948	2	10	1	Tuvo	2
1949	1	10	1	Had	3
1949	2	10	1	Tenido	3
1950	1	10	1	Hear	1
1950	2	10	1	Oír	1
1951	1	10	1	Heard	2
1951	2	10	1	Oyó	2
1952	1	10	1	Heard	3
1952	2	10	1	Oído	3
1953	1	10	1	Hold	1
1953	2	10	1	Sostener	1
1954	1	10	1	Held	2
1954	2	10	1	Sostuvo	2
1955	1	10	1	Held	3
1955	2	10	1	Sostenido	3
1956	1	10	1	Keep	1
1956	2	10	1	Mantener	1
1957	1	10	1	Kept	2
1957	2	10	1	Mantuvo	2
1958	1	10	1	Kept	3
1958	2	10	1	Mantenido	3
1959	1	10	1	Know	1
1959	2	10	1	Saber	1
1960	1	10	1	Knew	2
1960	2	10	1	Supo	2
1961	1	10	1	Known	3
1961	2	10	1	Sabido	3
1962	1	10	1	Leave	1
1962	2	10	1	Dejar	1
1963	1	10	1	Left	2
1963	2	10	1	Dejó	2
1964	1	10	1	Left	3
1964	2	10	1	Dejado	3
1965	1	10	1	Lose	1
1965	2	10	1	Perder	1
1966	1	10	1	Lost	2
1966	2	10	1	Perdió	2
1967	1	10	1	Lost	3
1967	2	10	1	Perdido	3
1968	1	10	1	Make	1
1968	2	10	1	Hacer	1
1969	1	10	1	Made	2
1969	2	10	1	Hizo	2
1970	1	10	1	Made	3
1970	2	10	1	Hecho	3
1971	1	10	1	Pay	1
1971	2	10	1	Pagar	1
1972	1	10	1	Paid	2
1972	2	10	1	Pagó	2
1973	1	10	1	Paid	3
1973	2	10	1	Pagado	3
1974	1	10	1	Put	1
1974	2	10	1	Poner	1
1975	1	10	1	Put	2
1975	2	10	1	Puso	2
1976	1	10	1	Put	3
1976	2	10	1	Puesto	3
1977	1	10	1	Read	1
1977	2	10	1	Leer	1
1978	1	10	1	Read	2
1978	2	10	1	Leyó	2
1979	1	10	1	Read	3
1979	2	10	1	Leído	3
1980	1	10	1	Say	1
1980	2	10	1	Decir	1
1981	1	10	1	Said	2
1981	2	10	1	Dijo	2
1982	1	10	1	Said	3
1982	2	10	1	Dicho	3
1983	1	10	1	See	1
1983	2	10	1	Ver	1
1984	1	10	1	Saw	2
1984	2	10	1	Vio	2
1985	1	10	1	Seen	3
1985	2	10	1	Visto	3
1986	1	10	1	Sell	1
1986	2	10	1	Vender	1
1987	1	10	1	Sold	2
1987	2	10	1	Vendió	2
1988	1	10	1	Sold	3
1988	2	10	1	Vendido	3
1989	1	10	1	Send	1
1989	2	10	1	Enviar	1
1990	1	10	1	Sent	2
1990	2	10	1	Envió	2
1991	1	10	1	Sent	3
1991	2	10	1	Enviado	3
1992	1	10	1	Sing	1
1992	2	10	1	Cantar	1
1993	1	10	1	Sang	2
1993	2	10	1	Cantó	2
1994	1	10	1	Sung	3
1994	2	10	1	Cantado	3
1995	1	10	1	Sit	1
1995	2	10	1	Sentarse	1
1996	1	10	1	Sat	2
1996	2	10	1	Se sentó	2
1997	1	10	1	Sat	3
1659	2	5	1	Contar	1
1660	1	5	1	Counted	2
1660	2	5	1	Contó / Contaba	2
1661	1	5	1	Counted	3
1661	2	5	1	Contado	3
1662	1	5	1	Cry	1
1662	2	5	1	Llorar / Gritar	1
1663	1	5	1	Cried	2
1663	2	5	1	Lloró / Lloraba	2
1664	1	5	1	Cried	3
1664	2	5	1	Llorado	3
1665	1	5	1	Die	1
1665	2	5	1	Morir	1
1666	1	5	1	Died	2
1666	2	5	1	Murió / Moría	2
1667	1	5	1	Died	3
1667	2	5	1	Muerto	3
1668	1	5	1	End	1
1668	2	5	1	Terminar / Finalizar	1
1669	1	5	1	Ended	2
1669	2	5	1	Terminó / Terminaba	2
1670	1	5	1	Ended	3
1670	2	5	1	Terminado	3
1671	1	5	1	Follow	1
1671	2	5	1	Seguir	1
1672	1	5	1	Followed	2
1672	2	5	1	Siguió / Seguía	2
1673	1	5	1	Followed	3
1673	2	5	1	Seguido	3
1674	1	5	1	Happen	1
1674	2	5	1	Suceder / Pasar	1
1675	1	5	1	Happened	2
1675	2	5	1	Sucedió / Sucedía	2
1676	1	5	1	Happened	3
1676	2	5	1	Sucedido	3
1677	1	5	1	Hate	1
1677	2	5	1	Odiar	1
1678	1	5	1	Hated	2
1678	2	5	1	Odió / Odiaba	2
1679	1	5	1	Hated	3
1679	2	5	1	Odiado	3
1680	1	5	1	Hope	1
1680	2	5	1	Esperar (con esperanza)	1
1681	1	5	1	Hoped	2
1681	2	5	1	Esperó / Esperaba	2
1682	1	5	1	Hoped	3
1682	2	5	1	Esperado	3
1683	1	5	1	Imagine	1
1683	2	5	1	Imaginar	1
1684	1	5	1	Imagined	2
1684	2	5	1	Imaginó / Imaginaba	2
1685	1	5	1	Imagined	3
1685	2	5	1	Imaginado	3
1686	1	5	1	Invite	1
1686	2	5	1	Invitar	1
1687	1	5	1	Invited	2
1687	2	5	1	Invitó / Invitaba	2
1688	1	5	1	Invited	3
1688	2	5	1	Invitado	3
1689	1	5	1	Kill	1
1689	2	5	1	Matar	1
1690	1	5	1	Killed	2
1690	2	5	1	Mató / Mataba	2
1691	1	5	1	Killed	3
1691	2	5	1	Matado	3
1692	1	5	1	Laugh	1
1692	2	5	1	Reírse	1
1693	1	5	1	Laughed	2
1693	2	5	1	Rio / Reía	2
1694	1	5	1	Laughed	3
1694	2	5	1	Reído	3
1695	1	5	1	Learn	1
1695	2	5	1	Aprender	1
1696	1	5	1	Learned	2
1696	2	5	1	Aprendió / Aprendía	2
1697	1	5	1	Learned	3
1697	2	5	1	Aprendido	3
1698	1	5	1	Love	1
1698	2	5	1	Amar / Encantar	1
1699	1	5	1	Loved	2
1699	2	5	1	Amó / Amaba	2
1700	1	5	1	Loved	3
1700	2	5	1	Amado	3
1701	1	5	1	Marry	1
1701	2	5	1	Casarse	1
1997	2	10	1	Sentado	3
1998	1	10	1	Sleep	1
1998	2	10	1	Dormir	1
1999	1	10	1	Slept	2
1999	2	10	1	Durmió	2
2000	1	10	1	Slept	3
2000	2	10	1	Dormido	3
2001	1	10	1	Speak	1
2001	2	10	1	Hablar	1
2002	1	10	1	Spoke	2
2002	2	10	1	Habló	2
2003	1	10	1	Spoken	3
2003	2	10	1	Hablado	3
2004	1	10	1	Take	1
2004	2	10	1	Tomar	1
2005	1	10	1	Took	2
2005	2	10	1	Tomó	2
2006	1	10	1	Taken	3
2006	2	10	1	Tomado	3
2007	1	10	1	Teach	1
2007	2	10	1	Enseñar	1
2008	1	10	1	Taught	2
2008	2	10	1	Enseñó	2
2009	1	10	1	Taught	3
2009	2	10	1	Enseñado	3
2010	1	10	1	Tell	1
2010	2	10	1	Contar	1
2011	1	10	1	Told	2
2011	2	10	1	Contó	2
2012	1	10	1	Told	3
2012	2	10	1	Contado	3
2013	1	10	1	Think	1
2013	2	10	1	Pensar	1
2014	1	10	1	Thought	2
2014	2	10	1	Pensó	2
2015	1	10	1	Thought	3
2015	2	10	1	Pensado	3
2016	1	10	1	Understand	1
2016	2	10	1	Entender	1
2017	1	10	1	Understood	2
2017	2	10	1	Entendió	2
2018	1	10	1	Understood	3
2018	2	10	1	Entendido	3
2019	1	10	1	Wear	1
2019	2	10	1	Llevar puesto	1
2020	1	10	1	Wore	2
2020	2	10	1	Llevó puesto	2
2021	1	10	1	Worn	3
2021	2	10	1	Llevado puesto	3
2022	1	10	1	Win	1
2022	2	10	1	Ganar	1
2023	1	10	1	Won	2
2023	2	10	1	Ganó	2
2024	1	10	1	Won	3
2024	2	10	1	Ganado	3
2025	1	10	1	Write	1
2025	2	10	1	Escribir	1
2026	1	10	1	Wrote	2
2026	2	10	1	Escribió	2
2027	1	10	1	Written	3
2027	2	10	1	Escrito	3
2244	1	5	1	Receive	1
2245	2	5	1	Recibir	1
2246	1	5	1	Received	2
2247	2	5	1	Recibió	2
2248	1	5	1	Received	3
2249	2	5	1	Recibido	3
2250	1	5	1	Reduce	1
2251	2	5	1	Reducir	1
2252	1	5	1	Reduced	2
2253	2	5	1	Redujo	2
2254	1	5	1	Reduced	3
2255	2	5	1	Reducido	3
2256	1	5	1	Refuse	1
2257	2	5	1	Rechazar	1
2258	1	5	1	Refused	2
2259	2	5	1	Rechazó	2
2260	1	5	1	Refused	3
2261	2	5	1	Rechazado	3
2262	1	5	1	Relax	1
2263	2	5	1	Relajar	1
2264	1	5	1	Relaxed	2
2265	2	5	1	Relajó	2
2266	1	5	1	Relaxed	3
2267	2	5	1	Relajado	3
2268	1	5	1	Remove	1
2269	2	5	1	Quitar	1
2270	1	5	1	Removed	2
2271	2	5	1	Quitó	2
2272	1	5	1	Removed	3
2273	2	5	1	Quitado	3
2274	1	5	1	Reply	1
2275	2	5	1	Responder	1
2276	1	5	1	Replied	2
2277	2	5	1	Respondió	2
2278	1	5	1	Replied	3
2279	2	5	1	Respondido	3
2280	1	5	1	Report	1
2281	2	5	1	Informar	1
2282	1	5	1	Reported	2
2283	2	5	1	Informó	2
2284	1	5	1	Reported	3
2285	2	5	1	Informado	3
2286	1	5	1	Request	1
2287	2	5	1	Solicitar	1
2288	1	5	1	Requested	2
2289	2	5	1	Solicitó	2
2290	1	5	1	Requested	3
2291	2	5	1	Solicitado	3
2292	1	5	1	Return	1
2293	2	5	1	Regresar	1
3222	1	10	1	Slide	1
2028	1	5	1	Add	1
2029	2	5	1	Añadir	1
2030	1	5	1	Added	2
2031	2	5	1	Añadió	2
2032	1	5	1	Added	3
2033	2	5	1	Añadido	3
2034	1	5	1	Agree	1
2035	2	5	1	Acordar	1
2036	1	5	1	Agreed	2
2037	2	5	1	Acordó	2
2038	1	5	1	Agreed	3
2039	2	5	1	Acordado	3
2040	1	5	1	Allow	1
2041	2	5	1	Permitir	1
2042	1	5	1	Allowed	2
2043	2	5	1	Permitió	2
2044	1	5	1	Allowed	3
2045	2	5	1	Permitido	3
2046	1	5	1	Appear	1
2047	2	5	1	Aparecer	1
2048	1	5	1	Appeared	2
2049	2	5	1	Apareció	2
2050	1	5	1	Appeared	3
2051	2	5	1	Aparecido	3
2052	1	5	1	Attack	1
2053	2	5	1	Atacar	1
2054	1	5	1	Attacked	2
2055	2	5	1	Atacó	2
2056	1	5	1	Attacked	3
2057	2	5	1	Atacado	3
2058	1	5	1	Brush	1
2059	2	5	1	Cepillar	1
2060	1	5	1	Brushed	2
2061	2	5	1	Cepilló	2
2062	1	5	1	Brushed	3
2063	2	5	1	Cepillado	3
2064	1	5	1	Camp	1
2065	2	5	1	Acampar	1
2066	1	5	1	Camped	2
2067	2	5	1	Acampó	2
2068	1	5	1	Camped	3
1702	1	5	1	Married	2
1702	2	5	1	Casó / Casaba	2
1703	1	5	1	Married	3
1703	2	5	1	Casado	3
1704	1	5	1	Miss	1
1704	2	5	1	Extrañar / Perder	1
1705	1	5	1	Missed	2
1705	2	5	1	Extrañó / Extrañaba	2
1706	1	5	1	Missed	3
1706	2	5	1	Extrañado	3
1707	1	5	1	Move	1
1707	2	5	1	Mover / Mudarse	1
1708	1	5	1	Moved	2
1708	2	5	1	Movió / Movía	2
1709	1	5	1	Moved	3
1709	2	5	1	Movido	3
1710	1	5	1	Offer	1
1710	2	5	1	Ofrecer	1
1711	1	5	1	Offered	2
1711	2	5	1	Ofreció / Ofrecía	2
1712	1	5	1	Offered	3
1712	2	5	1	Ofrecido	3
1713	1	5	1	Plan	1
1713	2	5	1	Planificar / Planear	1
1714	1	5	1	Planned	2
1714	2	5	1	Planificó / Planificaba	2
1715	1	5	1	Planned	3
1715	2	5	1	Planificado	3
1716	1	5	1	Prepare	1
1716	2	5	1	Preparar	1
1717	1	5	1	Prepared	2
1717	2	5	1	Preparó / Preparaba	2
1718	1	5	1	Prepared	3
1718	2	5	1	Preparado	3
1719	1	5	1	Promise	1
1719	2	5	1	Prometer	1
1720	1	5	1	Promised	2
1720	2	5	1	Prometió / Prometía	2
1721	1	5	1	Promised	3
1721	2	5	1	Prometido	3
1722	1	5	1	Receive	1
1722	2	5	1	Recibir	1
1723	1	5	1	Received	2
1723	2	5	1	Recibió / Recibía	2
1724	1	5	1	Received	3
1724	2	5	1	Recibido	3
1725	1	5	1	Repeat	1
1725	2	5	1	Repetir	1
1726	1	5	1	Repeated	2
1726	2	5	1	Repitió / Repetía	2
1727	1	5	1	Repeated	3
1727	2	5	1	Repetido	3
1728	1	5	1	Save	1
1728	2	5	1	Salvar / Guardar	1
1729	1	5	1	Saved	2
1729	2	5	1	Salvó / Salvaba	2
1730	1	5	1	Saved	3
1730	2	5	1	Salvado	3
1731	1	5	1	Smile	1
1731	2	5	1	Sonreír	1
1732	1	5	1	Smiled	2
1732	2	5	1	Sonrió / Sonreía	2
1733	1	5	1	Smiled	3
1733	2	5	1	Sonreído	3
1734	1	5	1	Stop	1
1734	2	5	1	Detener / Parar	1
1735	1	5	1	Stopped	2
1735	2	5	1	Detuvo / Detenía	2
1736	1	5	1	Stopped	3
1736	2	5	1	Detenido	3
1737	1	5	1	Touch	1
1737	2	5	1	Tocar	1
1738	1	5	1	Touched	2
1738	2	5	1	Tocó / Tocaba	2
1739	1	5	1	Touched	3
1739	2	5	1	Tocado	3
1740	1	5	1	Turn	1
1740	2	5	1	Girar / Voltear	1
1741	1	5	1	Turned	2
1741	2	5	1	Giró / Giraba	2
1742	1	5	1	Turned	3
1742	2	5	1	Girado	3
32	2	2	1	Bueno	1
33	1	2	1	Bad	1
34	2	2	1	Malo	1
35	1	2	1	Beautiful	1
36	2	2	1	Hermoso	1
37	1	2	1	Ugly	1
38	2	2	1	Feo	1
39	1	2	1	Large	1
40	2	2	1	Largo	1
41	1	2	1	Short	1
42	2	2	1	Corto	1
43	1	2	1	Cold	1
44	2	2	1	Frío	1
45	1	2	1	Hot	1
46	2	2	1	Caliente	1
47	1	2	1	Easy	1
48	2	2	1	Fácil	1
49	1	2	1	Hard	1
50	2	2	1	Difícil	1
51	1	2	1	Clean	1
52	2	2	1	Limpio	1
53	1	2	1	Dirty	1
54	2	2	1	Sucio	1
55	1	2	1	Strong	1
56	2	2	1	Fuerte	1
57	1	2	1	Weak	1
58	2	2	1	Débil	1
59	1	2	1	Smart	1
60	2	2	1	Inteligente	1
91	1	1	1	Body	1
92	2	1	1	Cuerpo	1
93	1	1	1	Head	1
94	2	1	1	Cabeza	1
95	1	1	1	Hand	1
96	2	1	1	Mano	1
97	1	1	1	Street	1
98	2	1	1	Calle	1
99	1	1	1	Door	1
100	2	1	1	Puerta	1
101	1	1	1	Window	1
102	2	1	1	Ventana	1
103	1	1	1	Face	1
104	2	1	1	Cara	1
105	1	1	1	Country	1
106	2	1	1	País	1
107	1	1	1	Number	1
108	2	1	1	Número	1
109	1	1	1	Night	1
110	2	1	1	Noche	1
111	1	1	1	Day	1
112	2	1	1	Día	1
113	1	1	1	Paper	1
114	2	1	1	Papel	1
115	1	1	1	Boy	1
116	2	1	1	Niño	1
117	1	1	1	Girl	1
118	2	1	1	Niña	1
119	1	1	1	Part	1
120	2	1	1	Parte	1
121	1	2	1	Early	1
122	2	2	1	Temprano	1
123	1	2	1	Late	1
124	2	2	1	Tarde	1
125	1	2	1	Young	1
126	2	2	1	Joven	1
127	1	2	1	Old	1
128	2	2	1	Viejo	1
129	1	2	1	Long	1
130	2	2	1	Largo	1
131	1	2	1	Little	1
132	2	2	1	Pequeño o poco	1
133	1	2	1	Great	1
134	2	2	1	Gran o genial	1
135	1	2	1	Right	1
136	2	2	1	Correcto o derecha	1
137	1	2	1	Small	1
138	2	2	1	Chico	1
139	1	2	1	Red	1
140	2	2	1	Rojo	1
141	1	2	1	Blue	1
142	2	2	1	Azul	1
143	1	2	1	White	1
144	2	2	1	Blanco	1
145	1	2	1	Black	1
146	2	2	1	Negro	1
147	1	2	1	Happy	1
148	2	2	1	Feliz	1
149	1	2	1	Sad	1
150	2	2	1	Triste	1
181	1	1	1	Head	1
182	2	1	1	Cabeza	1
183	1	1	1	Side	1
184	2	1	1	Lado	1
185	1	1	1	Point	1
186	2	1	1	Punto	1
188	2	1	1	Final o extremo	1
189	1	1	1	Air	1
190	2	1	1	Aire	1
191	1	1	1	Land	1
192	2	1	1	Tierra o suelo	1
193	1	1	1	Home	1
194	2	1	1	Hogar o casa	1
195	1	1	1	Mother	1
196	2	1	1	Madre	1
197	1	1	1	Father	1
198	2	1	1	Padre	1
199	1	1	1	Earth	1
200	2	1	1	Tierra (planeta)	1
201	1	1	1	Story	1
202	2	1	1	Historia o cuento	1
203	1	1	1	Boy	1
204	2	1	1	Muchacho	1
205	1	1	1	Girl	1
206	2	1	1	Muchacha	1
207	1	1	1	Plant	1
208	2	1	1	Planta	1
209	1	1	1	Food	1
210	2	1	1	Alimento	1
211	1	2	1	Important	1
212	2	2	1	Importante	1
213	1	2	1	Open	1
214	2	2	1	Abierto	1
215	1	2	1	Kind	1
216	2	2	1	Amable	1
217	1	2	1	Different	1
218	2	2	1	Diferente	1
219	1	2	1	Hard	1
220	2	2	1	Duro o difícil	1
221	1	2	1	Near	1
222	2	2	1	Cerca	1
223	1	2	1	Far	1
224	2	2	1	Lejos	1
225	1	2	1	Light	1
226	2	2	1	Ligero o claro	1
227	1	2	1	Dark	1
228	2	2	1	Oscuro	1
229	1	2	1	High	1
230	2	2	1	Alto	1
231	1	2	1	Low	1
232	2	2	1	Bajo	1
233	1	2	1	Simple	1
234	2	2	1	Simple	1
235	1	2	1	Own	1
236	2	2	1	Propio	1
237	1	2	1	Next	1
238	2	2	1	Siguiente	1
239	1	2	1	Last	1
240	2	2	1	Último	1
271	1	1	1	Stand	1
272	2	1	1	Soporte	1
273	1	1	1	Field	1
274	2	1	1	Campo	1
275	1	1	1	Fire	1
276	2	1	1	Fuego	1
277	1	1	1	News	1
278	2	1	1	Noticias	1
279	1	1	1	Bird	1
280	2	1	1	Pájaro	1
281	1	1	1	Area	1
282	2	1	1	Área	1
283	1	1	1	Problem	1
284	2	1	1	Problema	1
285	1	1	1	Piece	1
286	2	1	1	Pieza	1
287	1	1	1	Top	1
288	2	1	1	Cima	1
289	1	1	1	Bottom	1
290	2	1	1	Fondo	1
291	1	1	1	Rock	1
292	2	1	1	Roca	1
293	1	1	1	Order	1
294	2	1	1	Orden	1
295	1	1	1	Door	1
296	2	1	1	Puerta	1
297	1	1	1	Product	1
298	2	1	1	Producto	1
299	1	1	1	Wind	1
300	2	1	1	Viento	1
301	1	1	1	Color	1
302	2	1	1	Color	1
303	1	1	1	Ship	1
304	2	1	1	Barco	1
305	1	1	1	Half	1
306	2	1	1	Mitad	1
307	1	2	1	Full	1
308	2	2	1	Lleno	1
309	1	2	1	Empty	1
310	2	2	1	Vacío	1
311	1	2	1	Hot	1
312	2	2	1	Caliente	1
313	1	2	1	Cold	1
314	2	2	1	Frío	1
315	1	2	1	Warm	1
316	2	2	1	Cálido	1
317	1	2	1	Cool	1
318	2	2	1	Fresco	1
319	1	2	1	Sure	1
320	2	2	1	Seguro	1
321	1	2	1	Clear	1
322	2	2	1	Claro	1
323	1	2	1	Strong	1
324	2	2	1	Fuerte	1
325	1	2	1	Weak	1
326	2	2	1	Débil	1
327	1	2	1	Possible	1
328	2	2	1	Posible	1
329	1	2	1	Able	1
330	2	2	1	Capaz	1
331	1	2	1	Real	1
332	2	2	1	Real	1
333	1	2	1	True	1
334	2	2	1	Verdadero	1
335	1	2	1	False	1
336	2	2	1	Falso	1
371	1	1	2	Knowledge	1
372	2	1	2	Conocimiento	1
373	1	1	2	Environment	1
374	2	1	2	Medio ambiente	1
375	1	1	2	Opportunity	1
376	2	1	2	Oportunidad	1
377	1	1	2	Society	1
378	2	1	2	Sociedad	1
379	1	1	2	Journey	1
380	2	1	2	Trayecto	1
381	1	1	2	Health	1
382	2	1	2	Salud	1
383	1	1	2	Growth	1
384	2	1	2	Crecimiento	1
385	1	1	2	Century	1
386	2	1	2	Siglo	1
387	1	1	2	Purpose	1
388	2	1	2	Propósito	1
389	1	1	2	Effect	1
390	2	1	2	Efecto	1
391	1	1	2	Behavior	1
392	2	1	2	Comportamiento	1
393	1	1	2	Success	1
394	2	1	2	Éxito	1
395	1	1	2	Goal	1
396	2	1	2	Meta	1
397	1	1	2	Effort	1
398	2	1	2	Esfuerzo	1
399	1	1	2	Skill	1
400	2	1	2	Habilidad	1
401	1	1	2	Damage	1
402	2	1	2	Daño	1
403	1	1	2	Amount	1
404	2	1	2	Cantidad	1
405	1	1	2	Advice	1
406	2	1	2	Consejo	1
407	1	2	2	Useful	1
408	2	2	2	Útil	1
409	1	2	2	Reliable	1
410	2	2	2	Confiable	1
411	1	2	2	Average	1
412	2	2	2	Promedio	1
413	1	2	2	Common	1
414	2	2	2	Común	1
415	1	2	2	Strange	1
416	2	2	2	Extraño	1
417	1	2	2	Available	1
418	2	2	2	Disponible	1
419	1	2	2	Accurate	1
420	2	2	2	Preciso	1
421	1	2	2	Deep	1
422	2	2	2	Profundo	1
423	1	2	2	Shallow	1
424	2	2	2	Superficial	1
425	1	2	2	Sudden	1
426	2	2	2	Repentino	1
427	1	2	2	Empty	1
428	2	2	2	Vacío	1
429	1	2	2	Hollow	1
430	2	2	2	Hueco	1
431	1	2	2	Smooth	1
432	2	2	2	Suave o liso	1
433	1	2	2	Rough	1
434	2	2	2	Áspero	1
435	1	2	2	Valuable	1
436	2	2	2	Valioso	1
437	1	2	2	Useless	1
438	2	2	2	Inútil	1
471	1	1	3	Acquisition	1
472	2	1	3	Adquisición	1
473	1	1	3	Framework	1
474	2	1	3	Marco de trabajo	1
475	1	1	3	Bias	1
476	2	1	3	Sesgo	1
477	1	1	3	Hypothesis	1
478	2	1	3	Hipótesis	1
479	1	1	3	Infrastructure	1
480	2	1	3	Infraestructura	1
481	1	1	3	Legacy	1
482	2	1	3	Legado	1
483	1	1	3	Outcome	1
484	2	1	3	Resultado	1
485	1	1	3	Paradigm	1
486	2	1	3	Paradigma	1
487	1	1	3	Reliability	1
488	2	1	3	Fiabilidad	1
489	1	1	3	Constraint	1
490	2	1	3	Restricción	1
491	1	1	3	Endeavor	1
492	2	1	3	Esfuerzo o empeño	1
493	1	1	3	Insight	1
494	2	1	3	Percepción profunda	1
495	1	1	3	Welfare	1
496	2	1	3	Bienestar	1
497	1	1	3	Shortage	1
498	2	1	3	Escasez	1
499	1	1	3	Threshold	1
500	2	1	3	Umbral	1
501	1	1	3	Wealth	1
502	2	1	3	Riqueza	1
503	1	1	3	Hardship	1
504	2	1	3	Adversidad	1
505	1	2	3	Ambiguous	1
506	2	2	3	Ambiguo	1
507	1	2	3	Comprehensive	1
508	2	2	3	Integral o exhaustivo	1
509	1	2	3	Feasible	1
510	2	2	3	Factible	1
511	1	2	3	Implicit	1
512	2	2	3	Implícito	1
513	1	2	3	Inherent	1
514	2	2	3	Inherente	1
515	1	2	3	Obsolete	1
516	2	2	3	Obsoleto	1
517	1	2	3	Plausible	1
518	2	2	3	Plausible	1
519	1	2	3	Resilient	1
520	2	2	3	Resiliente	1
521	1	2	3	Subtle	1
522	2	2	3	Sutil	1
523	1	2	3	Sustainable	1
524	2	2	3	Sostenible	1
525	1	2	3	Vulnerable	1
526	2	2	3	Vulnerable	1
527	1	2	3	Wholistic	1
528	2	2	3	Holístico	1
529	1	2	3	Unprecedented	1
530	2	2	3	Sin precedentes	1
531	1	2	3	Scarcely	1
532	2	2	3	Escasamente	1
533	1	2	3	Useless	1
534	2	2	3	Inútil	1
571	1	4	1	I	1
572	2	4	1	Yo	1
573	1	4	1	You	1
574	2	4	1	Tú / Usted	1
575	1	4	1	He	1
576	2	4	1	Él	1
577	1	4	1	She	1
578	2	4	1	Ella	1
579	1	4	1	It	1
580	2	4	1	Eso / Ello	1
581	1	4	1	We	1
582	2	4	1	Nosotros	1
583	1	4	1	They	1
584	2	4	1	Ellos	1
585	1	4	1	Me	1
586	2	4	1	Mí / Me	1
587	1	4	1	Him	1
588	2	4	1	Él / Lo (objeto)	1
589	1	4	1	Her	1
590	2	4	1	Ella / La (objeto)	1
591	1	4	1	Us	1
592	2	4	1	Nosotros (objeto)	1
593	1	4	1	Them	1
594	2	4	1	Ellos / Las / Los (objeto)	1
595	1	4	1	Mine	1
596	2	4	1	Mío / Mía	1
597	1	4	1	Yours	1
598	2	4	1	Tuyo / Suyo	1
599	1	3	1	My	1
600	2	3	1	Mi (posesivo)	1
601	1	3	1	Your	1
602	2	3	1	Tu / Su (de usted)	1
603	1	3	1	His	1
604	2	3	1	Su (de él)	1
605	1	3	1	Her	1
606	2	3	1	Su (de ella)	1
607	1	3	1	Our	1
608	2	3	1	Nuestro	1
609	1	3	1	Their	1
610	2	3	1	Su (de ellos)	1
611	1	3	1	The	1
612	2	3	1	El / La / Los / Las	1
613	1	3	1	A	1
614	2	3	1	Un / Una	1
615	1	3	1	An	1
616	2	3	1	Un / Una (vocal)	1
617	1	3	1	This	1
618	2	3	1	Este / Esta	1
619	1	3	1	That	1
620	2	3	1	Ese / Aquel	1
621	1	3	1	These	1
622	2	3	1	Estos / Estas	1
623	1	3	1	Those	1
624	2	3	1	Esos / Aquellos	1
625	1	7	1	In	1
626	2	7	1	En / Dentro	1
627	1	7	1	On	1
628	2	7	1	En / Sobre	1
629	1	7	1	At	1
630	2	7	1	En (punto exacto)	1
631	1	7	1	Under	1
632	2	7	1	Debajo de	1
633	1	7	1	Over	1
634	2	7	1	Encima de / Sobre	1
635	1	7	1	Between	1
636	2	7	1	Entre (dos)	1
637	1	7	1	Behind	1
638	2	7	1	Detrás de	1
639	1	7	1	Next to	1
640	2	7	1	Al lado de	1
641	1	7	1	With	1
642	2	7	1	Con	1
643	1	7	1	Without	1
644	2	7	1	Sin	1
645	1	7	1	Before	1
646	2	7	1	Antes de	1
647	1	7	1	After	1
648	2	7	1	Después de	1
649	1	7	1	During	1
650	2	7	1	Durante	1
651	1	7	1	Against	1
652	2	7	1	Contra	1
653	1	7	1	About	1
654	2	7	1	Sobre / Acerca de	1
655	1	6	1	Always	1
656	2	6	1	Siempre	1
657	1	6	1	Never	1
658	2	6	1	Nunca	1
659	1	6	1	Often	1
660	2	6	1	A menudo	1
661	1	6	1	Sometimes	1
662	2	6	1	A veces	1
663	1	6	1	Usually	1
664	2	6	1	Usualmente	1
665	1	6	1	Now	1
666	2	6	1	Ahora	1
667	1	6	1	Later	1
668	2	6	1	Más tarde	1
669	1	6	1	Soon	1
670	2	6	1	Pronto	1
671	1	6	1	Today	1
672	2	6	1	Hoy	1
673	1	6	1	Yesterday	1
674	2	6	1	Ayer	1
675	1	6	1	Here	1
676	2	6	1	Aquí	1
677	1	6	1	There	1
678	2	6	1	Allí	1
679	1	6	1	Far	1
680	2	6	1	Lejos	1
681	1	6	1	Near	1
682	2	6	1	Cerca	1
683	1	6	1	Very	1
684	2	6	1	Muy	1
685	1	6	1	Too	1
686	2	6	1	Demasiado	1
687	1	6	1	Fast	1
688	2	6	1	Rápido	1
689	1	6	1	Slowly	1
690	2	6	1	Lentamente	1
691	1	8	1	And	1
692	2	8	1	Y	1
693	1	8	1	But	1
694	2	8	1	Pero	1
695	1	8	1	Or	1
696	2	8	1	O	1
697	1	8	1	Because	1
698	2	8	1	Porque	1
699	1	8	1	So	1
700	2	8	1	Así que / Entonces	1
701	1	8	1	If	1
702	2	8	1	Si (condicional)	1
703	1	8	1	Although	1
704	2	8	1	Aunque	1
705	1	8	1	Unless	1
706	2	8	1	A menos que	1
707	1	8	1	Until	1
708	2	8	1	Hasta que	1
709	1	8	1	While	1
710	2	8	1	Mientras	1
711	1	3	1	Every	1
712	2	3	1	Cada / Todos	1
713	1	3	1	Each	1
714	2	3	1	Cada uno	1
715	1	3	1	All	1
716	2	3	1	Todo / Todos	1
717	1	3	1	No	1
718	2	3	1	No / Ningún	1
719	1	9	1	Hello	1
720	2	9	1	Hola	1
721	1	9	1	Goodbye	1
722	2	9	1	Adiós	1
723	1	9	1	Please	1
724	2	9	1	Por favor	1
725	1	9	1	Thanks	1
726	2	9	1	Gracias	1
727	1	9	1	Yes	1
728	2	9	1	Sí	1
729	1	9	1	No	1
730	2	9	1	No	1
731	1	7	1	For	1
732	2	7	1	Para / Por	1
733	1	7	1	From	1
734	2	7	1	Desde / De	1
735	1	4	1	Someone	1
736	2	4	1	Alguien	1
737	1	4	1	Nobody	1
738	2	4	1	Nadie	1
739	1	4	1	Everything	1
740	2	4	1	Todo (cosa)	1
741	1	4	1	Something	1
742	2	4	1	Algo	1
743	1	6	1	Maybe	1
744	2	6	1	Tal vez / Quizás	1
745	1	6	1	Still	1
746	2	6	1	Todavía / Aún	1
747	1	6	1	Already	1
748	2	6	1	Ya	1
749	1	6	1	Yet	1
750	2	6	1	Todavía (negativo)	1
751	1	6	1	Together	1
752	2	6	1	Juntos	1
753	1	6	1	Alone	1
754	2	6	1	Solo	1
755	1	7	1	Above	1
756	2	7	1	Por encima de	1
757	1	7	1	Below	1
758	2	7	1	Por debajo de	1
759	1	7	1	Inside	1
760	2	7	1	Dentro de	1
761	1	7	1	Outside	1
762	2	7	1	Fuera de	1
763	1	8	1	As	1
764	2	8	1	Como (conector)	1
765	1	8	1	Than	1
766	2	8	1	Que (comparación)	1
767	1	9	1	Wow	1
768	2	9	1	Guau / Vaya	1
769	1	9	1	Oh	1
770	2	9	1	Oh	1
771	1	9	1	Help	1
772	2	9	1	Auxilio / Ayuda	1
773	1	9	1	Sorry	1
774	2	9	1	Lo siento / Perdón	1
775	1	3	1	Each	1
776	2	3	1	Cada	1
777	1	3	1	Another	1
778	2	3	1	Otro	1
779	1	3	1	Other	1
780	2	3	1	Otros / Otro	1
781	1	3	1	Many	1
782	2	3	1	Muchos	1
783	1	3	1	Much	1
784	2	3	1	Mucho	1
785	1	3	1	Few	1
786	2	3	1	Pocos	1
787	1	3	1	Little	1
788	2	3	1	Poco	1
789	1	8	1	Then	1
790	2	8	1	Entonces	1
791	1	6	1	Always	1
792	2	6	1	Siempre	1
793	1	4	1	Whoever	1
794	2	4	1	Quienquiera	1
795	1	4	1	Whatever	1
796	2	4	1	Lo que sea	1
797	1	3	1	Whose	1
798	2	3	1	De quién	1
799	1	9	1	Ouch	1
800	2	9	1	Ay (dolor)	1
801	1	9	1	Hey	1
802	2	9	1	Ey / Hola	1
803	1	3	1	Such	1
804	2	3	1	Tal / Semejante	1
805	1	7	1	Toward	1
806	2	7	1	Hacia	1
807	1	7	1	Upon	1
808	2	7	1	Sobre / Tras	1
809	1	7	1	Within	1
810	2	7	1	Dentro de / En el plazo de	1
811	1	7	1	Without	1
812	2	7	1	Sin	1
813	1	8	1	Since	1
814	2	8	1	Puesto que / Desde que	1
815	1	8	1	Unless	1
816	2	8	1	A menos que	1
817	1	6	1	Actually	1
818	2	6	1	En realidad	1
819	1	6	1	Already	1
820	2	6	1	Ya	1
821	1	6	1	Finally	1
822	2	6	1	Finalmente	1
823	1	6	1	Quickly	1
824	2	6	1	Rápidamente	1
825	1	6	1	Clearly	1
826	2	6	1	Claramente	1
827	1	6	1	Hardly	1
828	2	6	1	Apenas	1
829	1	6	1	Nearly	1
830	2	6	1	Casi	1
831	1	1	1	Teacher	1
832	2	1	1	Profesor / Maestro	1
833	1	1	1	Doctor	1
834	2	1	1	Doctor / Médico	1
835	1	1	1	Student	1
836	2	1	1	Estudiante	1
837	1	1	1	Kitchen	1
838	2	1	1	Cocina	1
839	1	1	1	Bedroom	1
840	2	1	1	Dormitorio	1
841	1	1	1	Bathroom	1
842	2	1	1	Baño	1
843	1	1	1	Table	1
844	2	1	1	Mesa	1
845	1	1	1	Chair	1
846	2	1	1	Silla	1
847	1	1	1	Car	1
848	2	1	1	Carro / Coche	1
849	1	1	1	Dog	1
850	2	1	1	Perro	1
851	1	1	1	Cat	1
852	2	1	1	Gato	1
853	1	1	1	Bread	1
854	2	1	1	Pan	1
855	1	1	1	Milk	1
856	2	1	1	Leche	1
857	1	1	1	Coffee	1
858	2	1	1	Café	1
859	1	1	1	Tea	1
860	2	1	1	Té	1
861	1	1	1	Apple	1
862	2	1	1	Manzana	1
863	1	1	1	Shirt	1
864	2	1	1	Camisa	1
865	1	1	1	Shoes	1
866	2	1	1	Zapatos	1
867	1	1	1	Key	1
868	2	1	1	Llave	1
869	1	1	1	Phone	1
870	2	1	1	Teléfono	1
871	1	1	1	Cloud	1
872	2	1	1	Nube	1
873	1	1	1	Rain	1
874	2	1	1	Lluvia	1
875	1	1	1	Star	1
876	2	1	1	Estrella	1
877	1	1	1	Sunlight	1
878	2	1	1	Luz solar	1
879	1	1	1	Heart	1
880	2	1	1	Corazón	1
881	1	2	1	Big	1
882	2	2	1	Grande	1
883	1	2	1	Fast	1
884	2	2	1	Rápido	1
885	1	2	1	Slow	1
886	2	2	1	Lento	1
887	1	2	1	Heavy	1
888	2	2	1	Pesado	1
889	1	2	1	Light	1
890	2	2	1	Ligero	1
891	1	2	1	Rich	1
892	2	2	1	Rico (dinero)	1
893	1	2	1	Poor	1
894	2	2	1	Pobre	1
895	1	2	1	Sweet	1
896	2	2	1	Dulce	1
897	1	2	1	Bitter	1
898	2	2	1	Amargo	1
899	1	2	1	Angry	1
900	2	2	1	Enojado	1
901	1	2	1	Quiet	1
902	2	2	1	Quieto / Silencioso	1
903	1	2	1	Loud	1
904	2	2	1	Ruidoso	1
905	1	2	1	Funny	1
906	2	2	1	Divertido / Gracioso	1
907	1	2	1	Serious	1
908	2	2	1	Serio	1
909	1	2	1	Brave	1
910	2	2	1	Valiente	1
911	1	2	1	Scared	1
912	2	2	1	Asustado	1
913	1	2	1	Tired	1
914	2	2	1	Cansado	1
915	1	2	1	Boring	1
916	2	2	1	Aburrido	1
917	1	2	1	Dry	1
918	2	2	1	Seco	1
919	1	2	1	Wet	1
920	2	2	1	Mojado	1
921	1	2	1	Soft	1
922	2	2	1	Blando / Suave	1
923	1	2	1	Hard	1
924	2	2	1	Duro	1
925	1	2	1	Expensive	1
926	2	2	1	Caro	1
927	1	2	1	Cheap	1
928	2	2	1	Barato	1
929	1	2	1	Young	1
930	2	2	1	Joven	1
991	1	1	1	Computer	1
992	2	1	1	Computadora / Ordenador	1
993	1	1	1	Screen	1
994	2	1	1	Pantalla	1
995	1	1	1	Keyboard	1
996	2	1	1	Teclado	1
997	1	1	1	Mouse	1
998	2	1	1	Ratón / Mouse	1
999	1	1	1	Office	1
1000	2	1	1	Oficina	1
1001	1	1	1	Job	1
1002	2	1	1	Trabajo / Empleo	1
1003	1	1	1	Boss	1
1004	2	1	1	Jefe	1
1005	1	1	1	Worker	1
1006	2	1	1	Trabajador	1
1007	1	1	1	Client	1
1008	2	1	1	Cliente	1
1009	1	1	1	Company	1
1010	2	1	1	Empresa / Compañía	1
1011	1	1	1	Meeting	1
1012	2	1	1	Reunión	1
1013	1	1	1	Message	1
1014	2	1	1	Mensaje	1
1015	1	1	1	Email	1
1016	2	1	1	Correo electrónico	1
1017	1	2	1	Polite	1
1018	2	2	1	Educado / Cortés	1
1019	1	2	1	Rude	1
1020	2	2	1	Grosero / Maleducado	1
1021	1	2	1	Kind	1
1022	2	2	1	Amable	1
1023	1	2	1	Nervous	1
1024	2	2	1	Nervioso	1
1025	1	2	1	Calm	1
1026	2	2	1	Calmado / Tranquilo	1
1027	1	2	1	Fast	1
1028	2	2	1	Veloz / Rápido	1
1029	1	2	1	Careful	1
1030	2	2	1	Cuidadoso	1
1031	1	2	1	Healthy	1
1032	2	2	1	Saludable / Sano	1
1033	1	2	1	Sick	1
1034	2	2	1	Enfermo	1
1035	1	2	1	Strong	1
1036	2	2	1	Fuerte	1
1071	1	1	1	Bread	1
1072	2	1	1	Pan	1
1073	1	1	1	Table	1
1074	2	1	1	Mesa	1
1075	1	1	1	Chair	1
1076	2	1	1	Silla	1
1077	1	1	1	Bottle	1
1078	2	1	1	Botella	1
1079	1	1	1	Glass	1
1080	2	1	1	Vaso	1
1081	1	1	1	Plate	1
1082	2	1	1	Plato	1
1083	1	1	1	Fork	1
1084	2	1	1	Tenedor	1
1085	1	1	1	Knife	1
1086	2	1	1	Cuchillo	1
1087	1	1	1	Spoon	1
1088	2	1	1	Cuchara	1
1089	1	1	1	Wall	1
1090	2	1	1	Pared	1
1091	1	1	1	Floor	1
1092	2	1	1	Suelo	1
1093	1	1	1	Roof	1
1094	2	1	1	Techo	1
1095	1	1	1	Garden	1
1096	2	1	1	Jardín	1
1097	1	1	1	Bed	1
1098	2	1	1	Cama	1
1099	1	1	1	Pillow	1
1100	2	1	1	Almohada	1
1101	1	1	1	Lamp	1
1102	2	1	1	Lámpara	1
1103	1	1	1	Box	1
1104	2	1	1	Caja	1
1105	1	1	1	Bag	1
1106	2	1	1	Bolsa	1
1107	1	1	1	Watch	1
1108	2	1	1	Reloj	1
1109	1	1	1	Pen	1
1110	2	1	1	Bolígrafo	1
1111	1	1	1	Pencil	1
1112	2	1	1	Lápiz	1
1113	1	1	1	Ring	1
1114	2	1	1	Anillo	1
1115	1	1	1	Hat	1
1116	2	1	1	Sombrero	1
1117	1	1	1	Coat	1
1118	2	1	1	Abrigo	1
1119	1	1	1	Pants	1
1120	2	1	1	Pantalones	1
1121	1	1	1	Dress	1
1122	2	1	1	Vestido	1
1123	1	1	1	Mountain	1
1124	2	1	1	Montaña	1
1125	1	1	1	River	1
1126	2	1	1	Río	1
1127	1	1	1	Sea	1
1128	2	1	1	Mar	1
1129	1	1	1	Beach	1
1130	2	1	1	Playa	1
1131	1	1	1	Park	1
1132	2	1	1	Parque	1
1133	1	1	1	Key	1
1134	2	1	1	Llave	1
1135	1	1	1	Clock	1
1136	2	1	1	Reloj de pared	1
1137	1	1	1	Mirror	1
1138	2	1	1	Espejo	1
1139	1	1	1	Bridge	1
1140	2	1	1	Puente	1
1141	1	1	1	Animal	1
1142	2	1	1	Animal	1
1143	1	1	1	Fish	1
1144	2	1	1	Pez	1
1145	1	1	1	Horse	1
1146	2	1	1	Caballo	1
1147	1	1	1	Cow	1
1148	2	1	1	Vaca	1
1149	1	1	1	Fruit	1
1150	2	1	1	Fruta	1
1151	1	1	1	Orange	1
1152	2	1	1	Naranja	1
1153	1	1	1	Yellow	1
1154	2	1	1	Amarillo	1
1155	1	1	1	Green	1
1156	2	1	1	Verde	1
1157	1	1	1	Letter	1
1158	2	1	1	Carta	1
1159	1	1	1	Map	1
1160	2	1	1	Mapa	1
1161	1	1	1	Gold	1
1162	2	1	1	Oro	1
1163	1	1	1	Silver	1
1164	2	1	1	Plata	1
1165	1	1	1	Wood	1
1166	2	1	1	Madera	1
1167	1	1	1	Stone	1
1168	2	1	1	Piedra	1
1169	1	1	1	Sky	1
1170	2	1	1	Cielo	1
1171	1	2	1	Fast	1
1172	2	2	1	Rápido	1
1173	1	2	1	Slow	1
1174	2	2	1	Lento	1
1175	1	2	1	Heavy	1
1176	2	2	1	Pesado	1
1177	1	2	1	Light	1
1178	2	2	1	Ligero	1
1179	1	2	1	Rich	1
1180	2	2	1	Rico	1
1181	1	2	1	Poor	1
1182	2	2	1	Pobre	1
1183	1	2	1	Sweet	1
1184	2	2	1	Dulce	1
1185	1	2	1	Bitter	1
1186	2	2	1	Amargo	1
1187	1	2	1	Salt	1
1188	2	2	1	Salado	1
1189	1	2	1	Sour	1
1190	2	2	1	Agrio	1
1191	1	2	1	Quiet	1
1192	2	2	1	Silencioso	1
1193	1	2	1	Loud	1
1194	2	2	1	Ruidoso	1
1195	1	2	1	Clean	1
1196	2	2	1	Limpio	1
1197	1	2	1	Dirty	1
1198	2	2	1	Sucio	1
1199	1	2	1	Dry	1
1200	2	2	1	Seco	1
1201	1	2	1	Wet	1
1202	2	2	1	Mojado	1
1203	1	2	1	Wide	1
1204	2	2	1	Ancho	1
1205	1	2	1	Narrow	1
1206	2	2	1	Estrecho	1
1207	1	2	1	Thick	1
1208	2	2	1	Grueso	1
1209	1	2	1	Thin	1
1210	2	2	1	Delgado	1
1211	1	2	1	Tired	1
1212	2	2	1	Cansado	1
1213	1	2	1	Hungry	1
1214	2	2	1	Hambriento	1
1215	1	2	1	Thirsty	1
1216	2	2	1	Sediento	1
1217	1	2	1	Brave	1
1218	2	2	1	Valiente	1
1219	1	2	1	Calm	1
1220	2	2	1	Calmado	1
1221	1	2	1	Angry	1
1222	2	2	1	Enojado	1
1223	1	2	1	Bored	1
1224	2	2	1	Aburrido	1
1225	1	2	1	Busy	1
1226	2	2	1	Ocupado	1
1227	1	2	1	Free	1
1228	2	2	1	Libre	1
1229	1	2	1	Safe	1
1230	2	2	1	Seguro	1
1231	1	2	1	Dangerous	1
1232	2	2	1	Peligroso	1
1233	1	2	1	Famous	1
1234	2	2	1	Famoso	1
1235	1	2	1	Strange	1
1236	2	2	1	Extraño	1
1237	1	2	1	Deep	1
1238	2	2	1	Profundo	1
1239	1	2	1	Shallow	1
1240	2	2	1	Superficial	1
1241	1	2	1	Expensive	1
1242	2	2	1	Caro	1
1243	1	2	1	Cheap	1
1244	2	2	1	Barato	1
1245	1	2	1	Cool	1
1246	2	2	1	Fresco	1
1247	1	2	1	Warm	1
1248	2	2	1	Cálido	1
1249	1	2	1	Round	1
1250	2	2	1	Redondo	1
1251	1	2	1	Square	1
1252	2	2	1	Cuadrado	1
1253	1	2	1	Flat	1
1254	2	2	1	Plano	1
1255	1	2	1	Shiny	1
1256	2	2	1	Brillante	1
1257	1	2	1	Clear	1
1258	2	2	1	Claro	1
1259	1	2	1	Dark	1
1260	2	2	1	Oscuro	1
1261	1	2	1	Gray	1
1262	2	2	1	Gris	1
1263	1	2	1	Brown	1
1264	2	2	1	Marrón	1
1265	1	2	1	Purple	1
1266	2	2	1	Morado	1
1267	1	2	1	Orange	1
1268	2	2	1	Naranja	1
1269	1	2	1	Pink	1
1270	2	2	1	Rosado	1
1371	1	1	1	Head	1
1372	2	1	1	Cabeza	1
1373	1	1	1	Arm	1
1374	2	1	1	Brazo	1
1375	1	1	1	Leg	1
1376	2	1	1	Pierna	1
1377	1	1	1	Hand	1
1378	2	1	1	Mano	1
1379	1	1	1	Foot	1
1380	2	1	1	Pie	1
1381	1	1	1	Eye	1
1382	2	1	1	Ojo	1
1383	1	1	1	Ear	1
1384	2	1	1	Oreja	1
1385	1	1	1	Nose	1
1386	2	1	1	Nariz	1
1387	1	1	1	Mouth	1
1388	2	1	1	Boca	1
1389	1	1	1	Finger	1
1390	2	1	1	Dedo	1
1391	1	1	1	Back	1
1392	2	1	1	Espalda	1
1393	1	1	1	Shoulder	1
1394	2	1	1	Hombro	1
1395	1	1	1	Knee	1
1396	2	1	1	Rodilla	1
1397	1	1	1	Doctor	1
1398	2	1	1	Doctor	1
1399	1	1	1	Nurse	1
1400	2	1	1	Enfermero	1
1401	1	1	1	Teacher	1
1402	2	1	1	Profesor	1
1403	1	1	1	Student	1
1404	2	1	1	Estudiante	1
1405	1	1	1	Engineer	1
1406	2	1	1	Ingeniero	1
1407	1	1	1	Lawyer	1
1408	2	1	1	Abogado	1
1409	1	1	1	Chef	1
1410	2	1	1	Cocinero	1
1411	1	1	1	Baker	1
1412	2	1	1	Panadero	1
1413	1	1	1	Farmer	1
1414	2	1	1	Granjero	1
1415	1	1	1	Pilot	1
1416	2	1	1	Piloto	1
1417	1	1	1	Police	1
1418	2	1	1	Policía	1
1419	1	1	1	Sun	1
1420	2	1	1	Sol	1
1421	1	1	1	Moon	1
1422	2	1	1	Luna	1
1423	1	1	1	Star	1
1424	2	1	1	Estrella	1
1425	1	1	1	Cloud	1
1426	2	1	1	Nube	1
1427	1	1	1	Rain	1
1428	2	1	1	Lluvia	1
1429	1	1	1	Snow	1
1430	2	1	1	Nieve	1
1431	1	1	1	Wind	1
1432	2	1	1	Viento	1
1433	1	1	1	Storm	1
1434	2	1	1	Tormenta	1
1435	1	1	1	Heat	1
1436	2	1	1	Calor	1
1437	1	1	1	Cold	1
1438	2	1	1	Frío	1
1439	1	1	1	City	1
1440	2	1	1	Ciudad	1
1441	1	1	1	Town	1
1442	2	1	1	Pueblo	1
1443	1	1	1	Street	1
1444	2	1	1	Calle	1
1445	1	1	1	House	1
1446	2	1	1	Casa	1
1447	1	1	1	Room	1
1448	2	1	1	Habitación	1
1449	1	1	1	Window	1
1450	2	1	1	Ventana	1
1451	1	1	1	Door	1
1452	2	1	1	Puerta	1
1453	1	1	1	Kitchen	1
1454	2	1	1	Cocina	1
1455	1	1	1	Park	1
1456	2	1	1	Parque	1
1457	1	1	1	Store	1
1458	2	1	1	Tienda	1
1459	1	1	1	Market	1
1460	2	1	1	Mercado	1
1461	1	1	1	Library	1
1462	2	1	1	Biblioteca	1
1463	1	1	1	Apple	1
1464	2	1	1	Manzana	1
1465	1	1	1	Banana	1
1466	2	1	1	Plátano	1
1467	1	1	1	Coffee	1
1468	2	1	1	Café	1
1469	1	1	1	Tea	1
1470	2	1	1	Té	1
1471	1	1	1	Water	1
1472	2	1	1	Agua	1
1473	1	1	1	Rice	1
1474	2	1	1	Arroz	1
1475	1	1	1	Sugar	1
1476	2	1	1	Azúcar	1
1477	1	1	1	Meat	1
1478	2	1	1	Carne	1
1479	1	1	1	Money	1
1480	2	1	1	Dinero	1
1481	1	1	1	Time	1
1482	2	1	1	Tiempo	1
1483	1	1	1	News	1
1484	2	1	1	Noticias	1
1485	1	1	1	Paper	1
1486	2	1	1	Papel	1
1487	1	1	1	Phone	1
1488	2	1	1	Teléfono	1
1489	1	1	1	Picture	1
1490	2	1	1	Foto	1
1491	1	1	1	Friend	1
1492	2	1	1	Amigo	1
1493	1	1	1	Enemy	1
1494	2	1	1	Enemigo	1
1495	1	1	1	Family	1
1496	2	1	1	Familia	1
1497	1	1	1	Morning	1
1498	2	1	1	Mañana	1
1499	1	1	1	Night	1
1500	2	1	1	Noche	1
1501	1	2	1	Big	1
1502	2	2	1	Grande	1
1503	1	2	1	Small	1
1504	2	2	1	Pequeño	1
1505	1	2	1	Long	1
1506	2	2	1	Largo	1
1507	1	2	1	Short	1
1508	2	2	1	Corto	1
1509	1	2	1	High	1
1510	2	2	1	Alto	1
1511	1	2	1	Low	1
1512	2	2	1	Bajo	1
1513	1	2	1	Wide	1
1514	2	2	1	Ancho	1
1515	1	2	1	Young	1
1516	2	2	1	Joven	1
1517	1	2	1	Old	1
1518	2	2	1	Viejo	1
1519	1	2	1	Hard	1
1520	2	2	1	Duro	1
1521	1	2	1	Soft	1
1522	2	2	1	Blando	1
1523	1	2	1	Strong	1
1524	2	2	1	Fuerte	1
1525	1	2	1	Weak	1
1526	2	2	1	Débil	1
1527	1	2	1	Happy	1
1528	2	2	1	Feliz	1
1529	1	2	1	Sad	1
1530	2	2	1	Triste	1
1531	1	2	1	New	1
1532	2	2	1	Nuevo	1
1533	1	2	1	First	1
1534	2	2	1	Primero	1
1535	1	2	1	Last	1
1536	2	2	1	Último	1
1537	1	2	1	Black	1
1538	2	2	1	Negro	1
1539	1	2	1	White	1
1540	2	2	1	Blanco	1
1541	1	2	1	Blue	1
1542	2	2	1	Azul	1
1543	1	2	1	Red	1
1544	2	2	1	Rojo	1
2069	2	5	1	Acampado	3
2070	1	5	1	Check	1
2071	2	5	1	Verificar	1
2072	1	5	1	Checked	2
2073	2	5	1	Verificó	2
2074	1	5	1	Checked	3
2075	2	5	1	Verificado	3
2076	1	5	1	Climb	1
2077	2	5	1	Escalar	1
2078	1	5	1	Climbed	2
2079	2	5	1	Escaló	2
2080	1	5	1	Climbed	3
2081	2	5	1	Escalado	3
2082	1	5	1	Cross	1
2083	2	5	1	Cruzar	1
2084	1	5	1	Crossed	2
2085	2	5	1	Cruzó	2
2086	1	5	1	Crossed	3
2087	2	5	1	Cruzado	3
2088	1	5	1	Deliver	1
2089	2	5	1	Entregar	1
2090	1	5	1	Delivered	2
2091	2	5	1	Entregó	2
2092	1	5	1	Delivered	3
2093	2	5	1	Entregado	3
2094	1	5	1	Depend	1
2095	2	5	1	Depender	1
2096	1	5	1	Depended	2
2097	2	5	1	Dependió	2
2098	1	5	1	Depended	3
2099	2	5	1	Dependido	3
2100	1	5	1	Describe	1
2101	2	5	1	Describir	1
2102	1	5	1	Described	2
2103	2	5	1	Describió	2
2104	1	5	1	Described	3
2105	2	5	1	Descrito	3
2106	1	5	1	Discover	1
2107	2	5	1	Descubrir	1
2108	1	5	1	Discovered	2
2109	2	5	1	Descubrió	2
2110	1	5	1	Discovered	3
2111	2	5	1	Descubierto	3
2112	1	5	1	Drop	1
2113	2	5	1	Soltar	1
2114	1	5	1	Dropped	2
2115	2	5	1	Soltó	2
2116	1	5	1	Dropped	3
2117	2	5	1	Soltado	3
2118	1	5	1	Earn	1
2119	2	5	1	Ganar	1
2120	1	5	1	Earned	2
2121	2	5	1	Ganó	2
2122	1	5	1	Earned	3
2123	2	5	1	Ganado	3
2124	1	5	1	Enter	1
2125	2	5	1	Entrar	1
2126	1	5	1	Entered	2
2127	2	5	1	Entró	2
2128	1	5	1	Entered	3
2129	2	5	1	Entrado	3
2130	1	5	1	Exercise	1
2131	2	5	1	Ejercitar	1
2132	1	5	1	Exercised	2
2133	2	5	1	Ejercitó	2
2134	1	5	1	Exercised	3
2135	2	5	1	Ejercitado	3
2136	1	5	1	Fill	1
2137	2	5	1	Llenar	1
2138	1	5	1	Filled	2
2139	2	5	1	Llenó	2
2140	1	5	1	Filled	3
2141	2	5	1	Llenado	3
2142	1	5	1	Fix	1
2143	2	5	1	Reparar	1
2144	1	5	1	Fixed	2
2145	2	5	1	Reparó	2
2146	1	5	1	Fixed	3
2147	2	5	1	Reparado	3
2148	1	5	1	Guess	1
2149	2	5	1	Adivinar	1
2150	1	5	1	Guessed	2
2151	2	5	1	Adivinó	2
2152	1	5	1	Guessed	3
2153	2	5	1	Adivinado	3
2154	1	5	1	Identify	1
2155	2	5	1	Identificar	1
2156	1	5	1	Identified	2
2157	2	5	1	Identificó	2
2158	1	5	1	Identified	3
2159	2	5	1	Identificado	3
2160	1	5	1	Introduce	1
2161	2	5	1	Presentar	1
2162	1	5	1	Introduced	2
2163	2	5	1	Presentó	2
2164	1	5	1	Introduced	3
2165	2	5	1	Presentado	3
2166	1	5	1	Kick	1
2167	2	5	1	Patear	1
2168	1	5	1	Kicked	2
2169	2	5	1	Pateó	2
2170	1	5	1	Kicked	3
2171	2	5	1	Pateado	3
2172	1	5	1	Lock	1
2173	2	5	1	Cerrar	1
2294	1	5	1	Returned	2
2295	2	5	1	Regresó	2
2296	1	5	1	Returned	3
2297	2	5	1	Regresado	3
2298	1	5	1	Search	1
2299	2	5	1	Buscar	1
2300	1	5	1	Searched	2
2301	2	5	1	Buscó	2
2302	1	5	1	Searched	3
2303	2	5	1	Buscado	3
2304	1	5	1	Select	1
2305	2	5	1	Seleccionar	1
2306	1	5	1	Selected	2
2307	2	5	1	Seleccionó	2
2308	1	5	1	Selected	3
2309	2	5	1	Seleccionado	3
2310	1	5	1	Shave	1
2311	2	5	1	Afeitar	1
2312	1	5	1	Shaved	2
2313	2	5	1	Afeitó	2
2314	1	5	1	Shaved	3
2315	2	5	1	Afeitado	3
2316	1	5	1	Shop	1
2317	2	5	1	Comprar	1
2318	1	5	1	Shopped	2
2319	2	5	1	Compró	2
2320	1	5	1	Shopped	3
2321	2	5	1	Comprado	3
2322	1	5	1	Shout	1
2323	2	5	1	Gritar	1
2324	1	5	1	Shouted	2
2325	2	5	1	Gritó	2
2326	1	5	1	Shouted	3
2327	2	5	1	Gritado	3
2328	1	5	1	Sign	1
2329	2	5	1	Firmar	1
2330	1	5	1	Signed	2
2331	2	5	1	Firmó	2
2332	1	5	1	Signed	3
2333	2	5	1	Firmado	3
2334	1	5	1	Solve	1
2335	2	5	1	Resolver	1
2336	1	5	1	Solved	2
2337	2	5	1	Resolvió	2
2338	1	5	1	Solved	3
2339	2	5	1	Resuelto	3
2340	1	5	1	Support	1
2341	2	5	1	Apoyar	1
2342	1	5	1	Supported	2
2343	2	5	1	Apoyó	2
2344	1	5	1	Supported	3
2345	2	5	1	Apoyado	3
2346	1	5	1	Thank	1
2347	2	5	1	Agradecer	1
2348	1	5	1	Thanked	2
2349	2	5	1	Agradeció	2
2350	1	5	1	Thanked	3
2351	2	5	1	Agradecido	3
2352	1	5	1	Touch	1
2353	2	5	1	Tocar	1
2354	1	5	1	Touched	2
2355	2	5	1	Tocó	2
2356	1	5	1	Touched	3
2357	2	5	1	Tocado	3
2358	1	5	1	Trust	1
2359	2	5	1	Confiar	1
2360	1	5	1	Trusted	2
2361	2	5	1	Confió	2
2362	1	5	1	Trusted	3
2363	2	5	1	Confiado	3
2364	1	5	1	Try	1
2365	2	5	1	Intentar	1
2366	1	5	1	Tried	2
2367	2	5	1	Intentó	2
2368	1	5	1	Tried	3
2369	2	5	1	Intentado	3
2370	1	5	1	Value	1
2371	2	5	1	Valorar	1
2372	1	5	1	Valued	2
2373	2	5	1	Valoró	2
2374	1	5	1	Valued	3
2375	2	5	1	Valorado	3
2376	1	5	1	Visit	1
2377	2	5	1	Visitar	1
2378	1	5	1	Visited	2
2379	2	5	1	Visitó	2
2380	1	5	1	Visited	3
2381	2	5	1	Visitado	3
2382	1	5	1	Warn	1
2383	2	5	1	Advertir	1
2384	1	5	1	Warned	2
2385	2	5	1	Advirtió	2
2386	1	5	1	Warned	3
2387	2	5	1	Advertido	3
2388	1	5	1	Wash	1
2389	2	5	1	Lavar	1
2390	1	5	1	Washed	2
2391	2	5	1	Lavó	2
2392	1	5	1	Washed	3
2393	2	5	1	Lavado	3
2394	1	5	1	Watch	1
2395	2	5	1	Observar	1
2396	1	5	1	Watched	2
2397	2	5	1	Observó	2
2398	1	5	1	Watched	3
2399	2	5	1	Observado	3
2400	1	5	1	Welcome	1
2401	2	5	1	Bienvenir	1
2402	1	5	1	Welcomed	2
2403	2	5	1	Bienvenido	2
2404	1	5	1	Welcomed	3
2405	2	5	1	Bienvenido	3
2406	1	5	1	Wonder	1
2407	2	5	1	Preguntarse	1
2408	1	5	1	Wondered	2
2409	2	5	1	Se preguntó	2
2410	1	5	1	Wondered	3
2411	2	5	1	Preguntado	3
2412	1	5	1	Worry	1
2413	2	5	1	Preocuparse	1
2414	1	5	1	Worried	2
2415	2	5	1	Se preocupó	2
2416	1	5	1	Worried	3
2417	2	5	1	Preocupado	3
2418	1	5	1	Breathe	1
2419	2	5	1	Respirar	1
2420	1	5	1	Breathed	2
2421	2	5	1	Respiró	2
2422	1	5	1	Breathed	3
2423	2	5	1	Respirado	3
2424	1	5	1	Care	1
2425	2	5	1	Cuidar	1
2426	1	5	1	Cared	2
2427	2	5	1	Cuidó	2
2428	1	5	1	Cared	3
2429	2	5	1	Cuidado	3
2430	1	5	1	Chop	1
2431	2	5	1	Picar	1
2432	1	5	1	Chopped	2
2433	2	5	1	Picó	2
2434	1	5	1	Chopped	3
2435	2	5	1	Picado	3
2436	1	5	1	Compare	1
2437	2	5	1	Comparar	1
2438	1	5	1	Compared	2
2439	2	5	1	Comparó	2
2440	1	5	1	Compared	3
2441	2	5	1	Comparado	3
2442	1	5	1	Complain	1
2443	2	5	1	Quejarse	1
2444	1	5	1	Complained	2
2445	2	5	1	Se quejó	2
2446	1	5	1	Complained	3
2447	2	5	1	Quejado	3
2448	1	5	1	Control	1
2449	2	5	1	Controlar	1
2450	1	5	1	Controlled	2
2451	2	5	1	Controló	2
2452	1	5	1	Controlled	3
2453	2	5	1	Controlado	3
2454	1	5	1	Copy	1
2455	2	5	1	Copiar	1
2456	1	5	1	Copied	2
2457	2	5	1	Copió	2
2458	1	5	1	Copied	3
2459	2	5	1	Copiado	3
2460	1	5	2	Advertise	1
2461	2	5	2	Anunciar	1
2462	1	5	2	Advertised	2
2463	2	5	2	Anunció	2
2464	1	5	2	Advertised	3
2465	2	5	2	Anunciado	3
2466	1	5	2	Advise	1
2467	2	5	2	Aconsejar	1
2468	1	5	2	Advised	2
2469	2	5	2	Aconsejó	2
2470	1	5	2	Advised	3
2471	2	5	2	Aconsejado	3
2472	1	5	2	Afford	1
2473	2	5	2	Costear	1
2474	1	5	2	Afforded	2
2475	2	5	2	Costeó	2
2476	1	5	2	Afforded	3
2477	2	5	2	Costeado	3
2478	1	5	2	Amuse	1
2479	2	5	2	Entretener	1
2480	1	5	2	Amused	2
2481	2	5	2	Entretuvo	2
2482	1	5	2	Amused	3
2483	2	5	2	Entretenido	3
2484	1	5	2	Analyze	1
2485	2	5	2	Analizar	1
2486	1	5	2	Analyzed	2
2487	2	5	2	Analizó	2
2488	1	5	2	Analyzed	3
2489	2	5	2	Analizado	3
2490	1	5	2	Approve	1
2491	2	5	2	Aprobar	1
2492	1	5	2	Approved	2
2493	2	5	2	Aprobó	2
2494	1	5	2	Approved	3
2495	2	5	2	Aprobado	3
2496	1	5	2	Attract	1
2497	2	5	2	Atraer	1
2498	1	5	2	Attracted	2
2499	2	5	2	Atrajo	2
2500	1	5	2	Attracted	3
2501	2	5	2	Atraído	3
2502	1	5	2	Banish	1
2503	2	5	2	Desterrar	1
2504	1	5	2	Banished	2
2505	2	5	2	Desterró	2
2506	1	5	2	Banished	3
2507	2	5	2	Desterrado	3
2508	1	5	2	Behave	1
2509	2	5	2	Comportar	1
2510	1	5	2	Behaved	2
2511	2	5	2	Comportó	2
2512	1	5	2	Behaved	3
2513	2	5	2	Comportado	3
2514	1	5	2	Calculate	1
2515	2	5	2	Calcular	1
2516	1	5	2	Calculated	2
2517	2	5	2	Calculó	2
2518	1	5	2	Calculated	3
2519	2	5	2	Calculado	3
2520	1	5	2	Challenge	1
2521	2	5	2	Desafiar	1
2522	1	5	2	Challenged	2
2523	2	5	2	Desafió	2
2524	1	5	2	Challenged	3
2525	2	5	2	Desafiado	3
2526	1	5	2	Claim	1
2527	2	5	2	Reclamar	1
2528	1	5	2	Claimed	2
2529	2	5	2	Reclamó	2
2530	1	5	2	Claimed	3
2531	2	5	2	Reclamado	3
2532	1	5	2	Confirm	1
2533	2	5	2	Confirmar	1
2534	1	5	2	Confirmed	2
2535	2	5	2	Confirmó	2
2536	1	5	2	Confirmed	3
2537	2	5	2	Confirmado	3
2538	1	5	2	Damage	1
2539	2	5	2	Dañar	1
2540	1	5	2	Damaged	2
2541	2	5	2	Dañó	2
2542	1	5	2	Damaged	3
2543	2	5	2	Dañado	3
2544	1	5	2	Decrease	1
2545	2	5	2	Disminuir	1
2546	1	5	2	Decreased	2
2547	2	5	2	Disminuyó	2
2548	1	5	2	Decreased	3
2549	2	5	2	Disminuido	3
2550	1	5	2	Delay	1
2551	2	5	2	Retrasar	1
2552	1	5	2	Delayed	2
2553	2	5	2	Retrasó	2
2554	1	5	2	Delayed	3
2555	2	5	2	Retrasado	3
2556	1	5	2	Deserve	1
2557	2	5	2	Merecer	1
2558	1	5	2	Deserved	2
2559	2	5	2	Mereció	2
2560	1	5	2	Deserved	3
2561	2	5	2	Merecido	3
2562	1	5	2	Destroy	1
2563	2	5	2	Destruir	1
2564	1	5	2	Destroyed	2
2565	2	5	2	Destruyó	2
2566	1	5	2	Destroyed	3
2567	2	5	2	Destruido	3
2568	1	5	2	Encourage	1
2569	2	5	2	Animar	1
2570	1	5	2	Encouraged	2
2571	2	5	2	Animó	2
2572	1	5	2	Encouraged	3
2573	2	5	2	Animado	3
2574	1	5	2	Establish	1
2575	2	5	2	Establecer	1
2576	1	5	2	Established	2
2577	2	5	2	Estableció	2
2578	1	5	2	Established	3
2579	2	5	2	Establecido	3
2580	1	5	2	Exaggerate	1
2581	2	5	2	Exagerar	1
2582	1	5	2	Exaggerated	2
2583	2	5	2	Exageró	2
2584	1	5	2	Exaggerated	3
2585	2	5	2	Exagerado	3
2586	1	5	2	Exclaim	1
2587	2	5	2	Exclamar	1
2588	1	5	2	Exclaimed	2
2589	2	5	2	Exclamó	2
2590	1	5	2	Exclaimed	3
2591	2	5	2	Exclamado	3
2592	1	5	2	Guarantee	1
2593	2	5	2	Garantizar	1
2594	1	5	2	Guaranteed	2
2595	2	5	2	Garantizó	2
2596	1	5	2	Guaranteed	3
2597	2	5	2	Garantizado	3
2598	1	5	2	Increase	1
2599	2	5	2	Aumentar	1
2600	1	5	2	Increased	2
2601	2	5	2	Aumentó	2
2602	1	5	2	Increased	3
2603	2	5	2	Aumentado	3
2604	1	5	2	Influence	1
2605	2	5	2	Influenciar	1
2606	1	5	2	Influenced	2
2607	2	5	2	Influenció	2
2608	1	5	2	Influenced	3
2609	2	5	2	Influenciado	3
2610	1	5	2	Inquire	1
2611	2	5	2	Consultar	1
2612	1	5	2	Inquired	2
2613	2	5	2	Consultó	2
2614	1	5	2	Inquired	3
2615	2	5	2	Consultado	3
2616	1	5	2	Inspect	1
2617	2	5	2	Inspecionar	1
2618	1	5	2	Inspected	2
2619	2	5	2	Inspeccionó	2
2620	1	5	2	Inspected	3
2621	2	5	2	Inspeccionado	3
2622	1	5	2	Instruct	1
2623	2	5	2	Instruir	1
2624	1	5	2	Instructed	2
2625	2	5	2	Instruyó	2
2626	1	5	2	Instructed	3
2627	2	5	2	Instruido	3
2628	1	5	2	Intend	1
2629	2	5	2	Pretender	1
2630	1	5	2	Intended	2
2631	2	5	2	Pretendió	2
2632	1	5	2	Intended	3
2633	2	5	2	Pretendido	3
2634	1	5	2	Interfere	1
2635	2	5	2	Interferir	1
2636	1	5	2	Interfered	2
2637	2	5	2	Interfirió	2
2638	1	5	2	Interfered	3
2639	2	5	2	Interferido	3
2640	1	5	2	Interrupt	1
2641	2	5	2	Interrumpir	1
2642	1	5	2	Interrupted	2
2643	2	5	2	Interrumpió	2
2644	1	5	2	Interrupted	3
2645	2	5	2	Interrumpido	3
2646	1	5	2	Invent	1
2647	2	5	2	Inventar	1
2648	1	5	2	Invented	2
2649	2	5	2	Inventó	2
2650	1	5	2	Invented	3
2651	2	5	2	Inventado	3
2652	1	5	2	Investigate	1
2653	2	5	2	Investigar	1
2654	1	5	2	Investigated	2
2655	2	5	2	Investigó	2
2656	1	5	2	Investigated	3
2657	2	5	2	Investigado	3
2658	1	5	2	Justify	1
2659	2	5	2	Justificar	1
2660	1	5	2	Justified	2
2661	2	5	2	Justificó	2
2662	1	5	2	Justified	3
2663	2	5	2	Justificado	3
2664	1	5	2	Maintain	1
2665	2	5	2	Mantener	1
2666	1	5	2	Maintained	2
2667	2	5	2	Mantuvo	2
2668	1	5	2	Maintained	3
2669	2	5	2	Mantenido	3
2670	1	5	2	Modify	1
2671	2	5	2	Modificar	1
2672	1	5	2	Modified	2
2673	2	5	2	Modificó	2
2674	1	5	2	Modified	3
2675	2	5	2	Modificado	3
2676	1	5	2	Neglect	1
2677	2	5	2	Descuidar	1
2678	1	5	2	Neglected	2
2679	2	5	2	Descuidó	2
2680	1	5	2	Neglected	3
2681	2	5	2	Descuidado	3
2682	1	5	2	Obtain	1
2683	2	5	2	Obtener	1
2684	1	5	2	Obtained	2
2685	2	5	2	Obtuvo	2
2686	1	5	2	Obtained	3
2687	2	5	2	Obtenido	3
2688	1	5	2	Oppose	1
2689	2	5	2	Oponer	1
2690	1	5	2	Opposed	2
2691	2	5	2	Opuso	2
2692	1	5	2	Opposed	3
2693	2	5	2	Opuesto	3
2694	1	5	2	Perceive	1
2695	2	5	2	Percibir	1
2696	1	5	2	Perceived	2
2697	2	5	2	Percibió	2
2698	1	5	2	Perceived	3
2699	2	5	2	Percibido	3
2700	1	5	2	Postpone	1
2701	2	5	2	Posponer	1
2702	1	5	2	Postponed	2
2703	2	5	2	Pospuso	2
2704	1	5	2	Postponed	3
2705	2	5	2	Pospuesto	3
2706	1	5	2	Practice	1
2707	2	5	2	Practicar	1
2708	1	5	2	Practiced	2
2709	2	5	2	Practicó	2
2710	1	5	2	Practiced	3
2711	2	5	2	Practicado	3
2712	1	5	2	Predict	1
2713	2	5	2	Predecir	1
2714	1	5	2	Predicted	2
2715	2	5	2	Predijo	2
2716	1	5	2	Predicted	3
2717	2	5	2	Predicho	3
2718	1	5	2	Proceed	1
2719	2	5	2	Proceder	1
2720	1	5	2	Proceeded	2
2721	2	5	2	Procedió	2
2722	1	5	2	Proceeded	3
2723	2	5	2	Procedido	3
2724	1	5	2	Prohibit	1
2725	2	5	2	Prohibir	1
2726	1	5	2	Prohibited	2
2727	2	5	2	Prohibió	2
2728	1	5	2	Prohibited	3
2729	2	5	2	Prohibido	3
2730	1	5	2	Propose	1
2731	2	5	2	Proponer	1
2732	1	5	2	Proposed	2
2733	2	5	2	Propuso	2
2734	1	5	2	Proposed	3
2735	2	5	2	Propuesto	3
2736	1	5	2	Protect	1
2737	2	5	2	Proteger	1
2738	1	5	2	Protected	2
2739	2	5	2	Protegió	2
2740	1	5	2	Protected	3
2741	2	5	2	Protegido	3
2742	1	5	2	Publish	1
2743	2	5	2	Publicar	1
2744	1	5	2	Published	2
2745	2	5	2	Publicó	2
2746	1	5	2	Published	3
2747	2	5	2	Publicado	3
2748	1	5	2	Punish	1
2749	2	5	2	Castigar	1
2750	1	5	2	Punished	2
2751	2	5	2	Castigó	2
2752	1	5	2	Punished	3
2753	2	5	2	Castigado	3
2754	1	5	2	Purchase	1
2755	2	5	2	Comprar	1
2756	1	5	2	Purchased	2
2757	2	5	2	Compró	2
2758	1	5	2	Purchased	3
2759	2	5	2	Comprado	3
2760	1	5	3	Abandon	1
2761	2	5	3	Abandonar	1
2762	1	5	3	Abandoned	2
2763	2	5	3	Abandonó	2
2764	1	5	3	Abandoned	3
2765	2	5	3	Abandonado	3
2766	1	5	3	Abolish	1
2767	2	5	3	Abolir	1
2768	1	5	3	Abolished	2
2769	2	5	3	Abolió	2
2770	1	5	3	Abolished	3
2771	2	5	3	Abolido	3
2772	1	5	3	Accumulate	1
2773	2	5	3	Acumular	1
2774	1	5	3	Accumulated	2
2775	2	5	3	Acumuló	2
2776	1	5	3	Accumulated	3
2777	2	5	3	Acumulado	3
2778	1	5	3	Administer	1
2779	2	5	3	Administrar	1
2780	1	5	3	Administered	2
2781	2	5	3	Administró	2
2782	1	5	3	Administered	3
2783	2	5	3	Administrado	3
2784	1	5	3	Anticipate	1
2785	2	5	3	Anticipar	1
2786	1	5	3	Anticipated	2
2787	2	5	3	Anticipó	2
2788	1	5	3	Anticipated	3
2789	2	5	3	Anticipado	3
2790	1	5	3	Assimilate	1
2791	2	5	3	Asimilar	1
2792	1	5	3	Assimilated	2
2793	2	5	3	Asimiló	2
2794	1	5	3	Assimilated	3
2795	2	5	3	Asimilado	3
2796	1	5	3	Coincide	1
2797	2	5	3	Coincidir	1
2798	1	5	3	Coincided	2
2799	2	5	3	Coincidió	2
2800	1	5	3	Coincided	3
2801	2	5	3	Coincidido	3
2802	1	5	3	Collaborate	1
2803	2	5	3	Colaborar	1
2804	1	5	3	Collaborated	2
2805	2	5	3	Colaboró	2
2806	1	5	3	Collaborated	3
2807	2	5	3	Colaborado	3
2808	1	5	3	Complicate	1
2809	2	5	3	Complicar	1
2810	1	5	3	Complicated	2
2811	2	5	3	Complicó	2
2812	1	5	3	Complicated	3
2813	2	5	3	Complicado	3
2814	1	5	3	Consolidate	1
2815	2	5	3	Consolidar	1
2816	1	5	3	Consolidated	2
2817	2	5	3	Consolidó	2
2818	1	5	3	Consolidated	3
2819	2	5	3	Consolidado	3
2820	1	5	3	Coordinate	1
2821	2	5	3	Coordinar	1
2822	1	5	3	Coordinated	2
2823	2	5	3	Coordinó	2
2824	1	5	3	Coordinated	3
2825	2	5	3	Coordinado	3
2826	1	5	3	Cultivate	1
2827	2	5	3	Cultivar	1
2828	1	5	3	Cultivated	2
2829	2	5	3	Cultivó	2
2830	1	5	3	Cultivated	3
2831	2	5	3	Cultivado	3
2832	1	5	3	Deteriorate	1
2833	2	5	3	Deteriorar	1
2834	1	5	3	Deteriorated	2
2835	2	5	3	Deterioró	2
2836	1	5	3	Deteriorated	3
2837	2	5	3	Deteriorado	3
2838	1	5	3	Differentiate	1
2839	2	5	3	Diferenciar	1
2840	1	5	3	Differentiated	2
2841	2	5	3	Diferenció	2
2842	1	5	3	Differentiated	3
2843	2	5	3	Diferenciado	3
2844	1	5	3	Diminish	1
2845	2	5	3	Diminuir	1
2846	1	5	3	Diminished	2
2847	2	5	3	Diminuó	2
2848	1	5	3	Diminished	3
2849	2	5	3	Diminuido	3
2850	1	5	3	Eradicate	1
2851	2	5	3	Erradicar	1
2852	1	5	3	Eradicated	2
2853	2	5	3	Erradicó	2
2854	1	5	3	Eradicated	3
2855	2	5	3	Erradicado	3
2856	1	5	3	Exterminate	1
2857	2	5	3	Exterminar	1
2858	1	5	3	Exterminated	2
2859	2	5	3	Exterminó	2
2860	1	5	3	Exterminated	3
2861	2	5	3	Exterminado	3
2862	1	5	3	Formulate	1
2863	2	5	3	Formular	1
2864	1	5	3	Formulated	2
2865	2	5	3	Formuló	2
2866	1	5	3	Formulated	3
2867	2	5	3	Formulado	3
2868	1	5	3	Illustrate	1
2869	2	5	3	Ilustrar	1
2870	1	5	3	Illustrated	2
2871	2	5	3	Ilustró	2
2872	1	5	3	Illustrated	3
2873	2	5	3	Ilustrado	3
2874	1	5	3	Inaugurate	1
2875	2	5	3	Inaugurar	1
2876	1	5	3	Inaugurated	2
2877	2	5	3	Inauguró	2
2878	1	5	3	Inaugurated	3
2879	2	5	3	Inaugurado	3
2880	1	5	3	Incorporate	1
2881	2	5	3	Incorporar	1
2882	1	5	3	Incorporated	2
2883	2	5	3	Incorporó	2
2884	1	5	3	Incorporated	3
2885	2	5	3	Incorporado	3
2886	1	5	3	Intimidate	1
2887	2	5	3	Intimidar	1
2888	1	5	3	Intimidated	2
2889	2	5	3	Intimidó	2
2890	1	5	3	Intimidated	3
2891	2	5	3	Intimidado	3
2892	1	5	3	Manipulate	1
2893	2	5	3	Manipular	1
2894	1	5	3	Manipulated	2
2895	2	5	3	Manipuló	2
2896	1	5	3	Manipulated	3
2897	2	5	3	Manipulado	3
2898	1	5	3	Modernize	1
2899	2	5	3	Modernizar	1
2900	1	5	3	Modernized	2
2901	2	5	3	Modernizó	2
2902	1	5	3	Modernized	3
2903	2	5	3	Modernizado	3
2904	1	5	3	Necessitate	1
2905	2	5	3	Necesitar	1
2906	1	5	3	Necessitated	2
2907	2	5	3	Necesitó	2
2908	1	5	3	Necessitated	3
2909	2	5	3	Necesitado	3
3223	2	10	1	Deslizar	1
3224	1	10	1	Slid	2
3225	2	10	1	Deslizó	2
3226	1	10	1	Slid	3
3227	2	10	1	Deslizado	3
3228	1	10	1	Spit	1
3229	2	10	1	Escupir	1
3230	1	10	1	Spat	2
3231	2	10	1	Escupió	2
3232	1	10	1	Spat	3
3233	2	10	1	Escupido	3
3234	1	10	1	Split	1
3235	2	10	1	Dividir	1
3236	1	10	1	Split	2
3237	2	10	1	Dividió	2
3238	1	10	1	Split	3
3239	2	10	1	Dividido	3
3240	1	10	1	Spoil	1
3241	2	10	1	Estropear	1
3242	1	10	1	Spoilt	2
3243	2	10	1	Estropeó	2
3244	1	10	1	Spoilt	3
3245	2	10	1	Estropeado	3
3246	1	10	1	Spread	1
3247	2	10	1	Extender	1
3248	1	10	1	Spread	2
3249	2	10	1	Extendió	2
3250	1	10	1	Spread	3
3251	2	10	1	Extendido	3
3252	1	10	1	Spring	1
3253	2	10	1	Brotar	1
3254	1	10	1	Sprang	2
3255	2	10	1	Brotó	2
3256	1	10	1	Sprung	3
3257	2	10	1	Brotado	3
3258	1	10	1	Steal	1
3259	2	10	1	Robar	1
3260	1	10	1	Stole	2
3261	2	10	1	Robó	2
3262	1	10	1	Stolen	3
3263	2	10	1	Robado	3
3264	1	10	1	Stick	1
3265	2	10	1	Pegar	1
3266	1	10	1	Stuck	2
3267	2	10	1	Pegó	2
3268	1	10	1	Stuck	3
3269	2	10	1	Pegado	3
3270	1	10	1	Sting	1
3271	2	10	1	Picar	1
3272	1	10	1	Stung	2
3273	2	10	1	Picó	2
3274	1	10	1	Stung	3
3275	2	10	1	Picado	3
3276	1	10	1	Strike	1
3277	2	10	1	Golpear	1
3278	1	10	1	Struck	2
3279	2	10	1	Golpeó	2
3280	1	10	1	Struck	3
3281	2	10	1	Golpeado	3
3282	1	10	1	Swear	1
3283	2	10	1	Jurar	1
3284	1	10	1	Swore	2
3285	2	10	1	Juró	2
3286	1	10	1	Sworn	3
3287	2	10	1	Jurado	3
3288	1	10	1	Sweep	1
3289	2	10	1	Barrer	1
3290	1	10	1	Swept	2
3291	2	10	1	Barrió	2
3292	1	10	1	Swept	3
3293	2	10	1	Barrido	3
3294	1	10	1	Swing	1
3295	2	10	1	Columpiar	1
3296	1	10	1	Swung	2
3297	2	10	1	Columpió	2
3298	1	10	1	Swung	3
3299	2	10	1	Columpiado	3
3300	1	10	1	Tear	1
3301	2	10	1	Rasgar	1
3302	1	10	1	Tore	2
3303	2	10	1	Rasgó	2
3304	1	10	1	Torn	3
3305	2	10	1	Rasgado	3
3306	1	10	1	Throw	1
3307	2	10	1	Lanzar	1
3308	1	10	1	Threw	2
3309	2	10	1	Lanzó	2
3310	1	10	1	Thrown	3
3311	2	10	1	Lanzado	3
3312	1	10	1	Wake	1
3313	2	10	1	Despertar	1
3314	1	10	1	Woke	2
3315	2	10	1	Despertó	2
3316	1	10	1	Woken	3
3317	2	10	1	Despertado	3
3318	1	10	1	Weep	1
3319	2	10	1	Llorar	1
3320	1	10	1	Wept	2
3321	2	10	1	Lloró	2
3322	1	10	1	Wept	3
3323	2	10	1	Llorado	3
3324	1	10	1	Withdraw	1
3325	2	10	1	Retirar	1
3326	1	10	1	Withdrew	2
3327	2	10	1	Retiró	2
3328	1	10	1	Withdrawn	3
3329	2	10	1	Retirado	3
3330	1	10	1	Wring	1
3331	2	10	1	Exprimir	1
3332	1	10	1	Wrung	2
3333	2	10	1	Exprimió	2
3334	1	10	1	Wrung	3
3335	2	10	1	Exprimido	3
3336	1	10	1	Thrive	1
3337	2	10	1	Prosperar	1
3338	1	10	1	Throve	2
3339	2	10	1	Prosperó	2
3340	1	10	1	Thriven	3
3341	2	10	1	Prosperado	3
3342	1	10	1	Undergo	1
3343	2	10	1	Sufrir	1
3344	1	10	1	Underwent	2
3345	2	10	1	Sufrió	2
3346	1	10	1	Undergone	3
3347	2	10	1	Sufrido	3
3348	1	10	1	Weave	1
3349	2	10	1	Tejer	1
3350	1	10	1	Wove	2
3351	2	10	1	Tejió	2
3352	1	10	1	Woven	3
3353	2	10	1	Tejido	3
3354	1	10	1	Shrink	1
3355	2	10	1	Encoger	1
3356	1	10	1	Shrank	2
3357	2	10	1	Encogió	2
3358	1	10	1	Shrunk	3
3359	2	10	1	Encogido	3
3360	1	10	2	Arise	1
3361	2	10	2	Surgir	1
3362	1	10	2	Arose	2
3363	2	10	2	Surgió	2
3364	1	10	2	Arisen	3
3365	2	10	2	Surgido	3
3366	1	10	2	Awake	1
3367	2	10	2	Despertar	1
3368	1	10	2	Awoke	2
3369	2	10	2	Despertó	2
3370	1	10	2	Awoken	3
3371	2	10	2	Despertado	3
3372	1	10	2	Bear	1
3373	2	10	2	Soportar	1
3374	1	10	2	Bore	2
3375	2	10	2	Soportó	2
3376	1	10	2	Borne	3
3377	2	10	2	Soportado	3
3378	1	10	2	Beat	1
3379	2	10	2	Golpear	1
3380	1	10	2	Beat	2
3381	2	10	2	Golpeó	2
3382	1	10	2	Beaten	3
3383	2	10	2	Golpeado	3
3384	1	10	2	Bind	1
3385	2	10	2	Atar	1
3386	1	10	2	Bound	2
3387	2	10	2	Ató	2
3388	1	10	2	Bound	3
3389	2	10	2	Atado	3
3390	1	10	2	Breed	1
3391	2	10	2	Criar	1
3392	1	10	2	Bred	2
3393	2	10	2	Crió	2
3394	1	10	2	Bred	3
3395	2	10	2	Criado	3
3396	1	10	2	Broadcast	1
3397	2	10	2	Transmitir	1
3398	1	10	2	Broadcast	2
3399	2	10	2	Transmitió	2
3400	1	10	2	Broadcast	3
3401	2	10	2	Transmitido	3
3402	1	10	2	Cling	1
3403	2	10	2	Agarrarse	1
3404	1	10	2	Clung	2
3405	2	10	2	Se agarró	2
3406	1	10	2	Clung	3
3407	2	10	2	Agarrado	3
3408	1	10	2	Creep	1
3409	2	10	2	Arrastrar	1
3410	1	10	2	Crept	2
3411	2	10	2	Arrastró	2
3412	1	10	2	Crept	3
3413	2	10	2	Arrastrado	3
3414	1	10	2	Flee	1
3415	2	10	2	Huir	1
3416	1	10	2	Fled	2
3417	2	10	2	Huyó	2
3418	1	10	2	Fled	3
3419	2	10	2	Huido	3
3420	1	10	2	Fling	1
3421	2	10	2	Arrojar	1
3422	1	10	2	Flung	2
3423	2	10	2	Arrojó	2
3424	1	10	2	Flung	3
3425	2	10	2	Arrojado	3
3426	1	10	2	Forbid	1
3427	2	10	2	Prohibir	1
3428	1	10	2	Forbade	2
3429	2	10	2	Prohibió	2
3430	1	10	2	Forbidden	3
3431	2	10	2	Prohibido	3
3432	1	10	2	Forecast	1
3433	2	10	2	Pronosticar	1
3434	1	10	2	Forecast	2
3435	2	10	2	Pronosticó	2
3436	1	10	2	Forecast	3
3437	2	10	2	Pronosticado	3
3438	1	10	2	Foresee	1
3439	2	10	2	Prever	1
3440	1	10	2	Foresaw	2
3441	2	10	2	Previó	2
3442	1	10	2	Foreseen	3
3443	2	10	2	Previsto	3
3444	1	10	2	Kneel	1
3445	2	10	2	Arrodillarse	1
3446	1	10	2	Knelt	2
3447	2	10	2	Se arrodilló	2
3448	1	10	2	Knelt	3
3449	2	10	2	Arrodillado	3
3450	1	10	2	Leap	1
3451	2	10	2	Saltar	1
3452	1	10	2	Leapt	2
3453	2	10	2	Saltó	2
3454	1	10	2	Leapt	3
3455	2	10	2	Saltado	3
3456	1	10	2	Mow	1
3457	2	10	2	Segar	1
3458	1	10	2	Mowed	2
3459	2	10	2	Segó	2
3460	1	10	2	Mown	3
3461	2	10	2	Segado	3
3462	1	10	2	Overhear	1
3463	2	10	2	Oír por casualidad	1
3464	1	10	2	Overheard	2
3465	2	10	2	Oyó por casualidad	2
3466	1	10	2	Overheard	3
3467	2	10	2	Oído por casualidad	3
3468	1	10	2	Seek	1
3469	2	10	2	Buscar	1
3470	1	10	2	Sought	2
3471	2	10	2	Buscó	2
3472	1	10	2	Sought	3
3473	2	10	2	Buscado	3
3474	1	10	2	Shed	1
3475	2	10	2	Derramar	1
3476	1	10	2	Shed	2
3477	2	10	2	Derramó	2
3478	1	10	2	Shed	3
3479	2	10	2	Derramado	3
3480	1	10	2	Slay	1
3481	2	10	2	Asesinar	1
3482	1	10	2	Slew	2
3483	2	10	2	Asesinó	2
3484	1	10	2	Slain	3
3485	2	10	2	Asesinado	3
3486	1	10	2	Sling	1
3487	2	10	2	Lanzar	1
3488	1	10	2	Slung	2
3489	2	10	2	Lanzó	2
3490	1	10	2	Slung	3
3491	2	10	2	Lanzado	3
3492	1	10	2	Slink	1
3493	2	10	2	Escabullirse	1
3494	1	10	2	Slunk	2
3495	2	10	2	Se escabulló	2
3496	1	10	2	Slunk	3
3497	2	10	2	Escabullido	3
3498	1	10	2	Slit	1
3499	2	10	2	Cortar	1
3500	1	10	2	Slit	2
3501	2	10	2	Cortó	2
3502	1	10	2	Slit	3
3503	2	10	2	Cortado	3
3504	1	10	2	Spin	1
3505	2	10	2	Girar	1
3506	1	10	2	Spun	2
3507	2	10	2	Giró	2
3508	1	10	2	Spun	3
3509	2	10	2	Girado	3
3510	1	10	2	Spit	1
3511	2	10	2	Escupir	1
3512	1	10	2	Spat	2
3513	2	10	2	Escupió	2
3514	1	10	2	Spat	3
3515	2	10	2	Escupido	3
3516	1	10	2	Stride	1
3517	2	10	2	Dar zancadas	1
3518	1	10	2	Strode	2
3519	2	10	2	Dio zancadas	2
3520	1	10	2	Stridden	3
3521	2	10	2	Dado zancadas	3
3522	1	10	2	String	1
3523	2	10	2	Encordar	1
3524	1	10	2	Strung	2
3525	2	10	2	Encordó	2
3526	1	10	2	Strung	3
3527	2	10	2	Encordado	3
3528	1	10	2	Strive	1
3529	2	10	2	Esforzarse	1
3530	1	10	2	Strove	2
3531	2	10	2	Se esforzó	2
3532	1	10	2	Striven	3
3533	2	10	2	Esforzado	3
3534	1	10	2	Sweep	1
3535	2	10	2	Barrer	1
3536	1	10	2	Swept	2
3537	2	10	2	Barrió	2
3538	1	10	2	Swept	3
3539	2	10	2	Barrido	3
3540	1	10	2	Tread	1
3541	2	10	2	Pisar	1
3542	1	10	2	Trod	2
3543	2	10	2	Pisó	2
3544	1	10	2	Trodden	3
3545	2	10	2	Pisado	3
3546	1	10	2	Uphold	1
3547	2	10	2	Defender	1
3548	1	10	2	Upheld	2
3549	2	10	2	Defendió	2
3550	1	10	2	Upheld	3
3551	2	10	2	Defendido	3
3552	1	10	2	Weep	1
3553	2	10	2	Llorar	1
3554	1	10	2	Wept	2
3555	2	10	2	Lloró	2
3556	1	10	2	Wept	3
3557	2	10	2	Llorado	3
3558	1	10	2	Wind	1
3559	2	10	2	Envolver	1
3560	1	10	2	Wound	2
3561	2	10	2	Envolvió	2
3562	1	10	2	Wound	3
3563	2	10	2	Enuelto	3
3564	1	10	2	Withhold	1
3565	2	10	2	Retener	1
3566	1	10	2	Withheld	2
3567	2	10	2	Retuvo	2
3568	1	10	2	Withheld	3
3569	2	10	2	Retenido	3
3570	1	10	2	Beget	1
3571	2	10	2	Engendrar	1
3572	1	10	2	Begot	2
3573	2	10	2	Engendró	2
3574	1	10	2	Begotten	3
3575	2	10	2	Engendrado	3
3576	1	10	2	Beseech	1
3577	2	10	2	Suplicar	1
3578	1	10	2	Besought	2
3579	2	10	2	Suplicó	2
3580	1	10	2	Besought	3
3581	2	10	2	Suplicado	3
3582	1	10	2	Chide	1
3583	2	10	2	Reprender	1
3584	1	10	2	Chid	2
3585	2	10	2	Reprendió	2
3586	1	10	2	Chidden	3
3587	2	10	2	Reprendido	3
3588	1	10	2	Cleave	1
3589	2	10	2	Hender	1
3590	1	10	2	Cleft	2
3591	2	10	2	Hendió	2
3592	1	10	2	Cleft	3
3593	2	10	2	Hendido	3
3594	1	10	2	Gird	1
3595	2	10	2	Ceñir	1
3596	1	10	2	Girt	2
3597	2	10	2	Ciñó	2
3598	1	10	2	Girt	3
3599	2	10	2	Ceñido	3
3600	1	10	2	Hew	1
3601	2	10	2	Tallar	1
3602	1	10	2	Hewed	2
3603	2	10	2	Talló	2
3604	1	10	2	Hewn	3
3605	2	10	2	Tallado	3
3606	1	10	2	Lade	1
3607	2	10	2	Cargar	1
3608	1	10	2	Laded	2
3609	2	10	2	Cargó	2
3610	1	10	2	Laden	3
3611	2	10	2	Cargado	3
3612	1	10	2	Rend	1
3613	2	10	2	Desgarrar	1
3614	1	10	2	Rent	2
3615	2	10	2	Desgarró	2
3616	1	10	2	Rent	3
3617	2	10	2	Desgarrado	3
3618	1	10	2	Smite	1
3619	2	10	2	Golpear duramente	1
3620	1	10	2	Smote	2
3621	2	10	2	Golpeó duramente	2
3622	1	10	2	Smitten	3
3623	2	10	2	Golpeado duramente	3
3624	1	10	2	Sow	1
3625	2	10	2	Sembrar	1
3626	1	10	2	Sowed	2
3627	2	10	2	Sembró	2
3628	1	10	2	Sown	3
3629	2	10	2	Sembrado	3
3630	1	10	2	Strew	1
3631	2	10	2	Esparcir	1
3632	1	10	2	Strewed	2
3633	2	10	2	Esparció	2
3634	1	10	2	Strewn	3
3635	2	10	2	Esparcido	3
3636	1	10	2	Sunder	1
3637	2	10	2	Separar	1
3638	1	10	2	Sundered	2
3639	2	10	2	Separó	2
3640	1	10	2	Sundered	3
3641	2	10	2	Separado	3
3642	1	10	2	Thrust	1
3643	2	10	2	Empujar	1
3644	1	10	2	Thrust	2
3645	2	10	2	Empujó	2
3646	1	10	2	Thrust	3
3647	2	10	2	Empujado	3
3648	1	10	2	Vex	1
3649	2	10	2	Irritar	1
3650	1	10	2	Vexed	2
3651	2	10	2	Irritó	2
3652	1	10	2	Vexed	3
3653	2	10	2	Irritado	3
3654	1	10	2	Wed	1
3655	2	10	2	Casar	1
3656	1	10	2	Wedded	2
3657	2	10	2	Casó	2
3658	1	10	2	Wedded	3
3659	2	10	2	Casado	3
3660	1	10	3	Abide	1
3661	2	10	3	Acatar	1
3662	1	10	3	Abode	2
3663	2	10	3	Acató	2
3664	1	10	3	Abode	3
3665	2	10	3	Acatado	3
3666	1	10	3	Belie	1
3667	2	10	3	Desmentir	1
3668	1	10	3	Belied	2
3669	2	10	3	Desmintió	2
3670	1	10	3	Belied	3
3671	2	10	3	Desmentido	3
3672	1	10	3	Beset	1
3673	2	10	3	Acosar	1
3674	1	10	3	Beset	2
3675	2	10	3	Acosó	2
3676	1	10	3	Beset	3
3677	2	10	3	Acosado	3
3678	1	10	3	Bestride	1
3679	2	10	3	Montar a horcajadas	1
3680	1	10	3	Bestrode	2
3681	2	10	3	Montó a horcajadas	2
3682	1	10	3	Bestridden	3
3683	2	10	3	Montado a horcajadas	3
3684	1	10	3	Betake	1
3685	2	10	3	Dirigirse	1
3686	1	10	3	Betook	2
3687	2	10	3	Se dirigió	2
3688	1	10	3	Betaken	3
3689	2	10	3	Dirigido	3
3690	1	10	3	Blent	1
3691	2	10	3	Mezclar	1
3692	1	10	3	Blent	2
3693	2	10	3	Mezcló	2
3694	1	10	3	Blent	3
3695	2	10	3	Mezclado	3
3696	1	10	3	Clothe	1
3697	2	10	3	Vestir	1
3698	1	10	3	Clad	2
3699	2	10	3	Vistió	2
3700	1	10	3	Clad	3
3701	2	10	3	Vestido	3
3702	1	10	3	Disprove	1
3703	2	10	3	Refutar	1
3704	1	10	3	Disproved	2
3705	2	10	3	Refutó	2
3706	1	10	3	Disproven	3
3707	2	10	3	Refutado	3
3708	1	10	3	Dwell	1
3709	2	10	3	Habitar	1
3710	1	10	3	Dwelt	2
3711	2	10	3	Habitó	2
3712	1	10	3	Dwelt	3
3713	2	10	3	Habitado	3
3714	1	10	3	Gainsay	1
3715	2	10	3	Contradecir	1
3716	1	10	3	Gainsaid	2
3717	2	10	3	Contradijo	2
3718	1	10	3	Gainsaid	3
3719	2	10	3	Contradicho	3
3720	1	10	3	Gild	1
3721	2	10	3	Dorar	1
3722	1	10	3	Gilt	2
3723	2	10	3	Doró	2
3724	1	10	3	Gilt	3
3725	2	10	3	Dorado	3
3726	1	10	3	Gird	1
3727	2	10	3	Ceñir	1
3728	1	10	3	Girt	2
3729	2	10	3	Ciñó	2
3730	1	10	3	Girt	3
3731	2	10	3	Ceñido	3
3732	1	10	3	Grave	1
3733	2	10	3	Grabar	1
3734	1	10	3	Graved	2
3735	2	10	3	Grabó	2
3736	1	10	3	Graven	3
3737	2	10	3	Grabado	3
3738	1	10	3	Hamstring	1
3739	2	10	3	Incapacitar	1
3740	1	10	3	Hamstrung	2
3741	2	10	3	Incapacitó	2
3742	1	10	3	Hamstrung	3
3743	2	10	3	Incapacitado	3
3744	1	10	3	Inlay	1
3745	2	10	3	Incrustar	1
3746	1	10	3	Inlaid	2
3747	2	10	3	Incrustó	2
3748	1	10	3	Inlaid	3
3749	2	10	3	Incrustado	3
3750	1	10	3	Misbecome	1
3751	2	10	3	Desacreditar	1
3752	1	10	3	Misbecame	2
3753	2	10	3	Desacreditó	2
3754	1	10	3	Misbecome	3
3755	2	10	3	Desacreditado	3
3756	1	10	3	Miscast	1
3757	2	10	3	Asignar mal un papel	1
3758	1	10	3	Miscast	2
3759	2	10	3	Asignó mal un papel	2
3760	1	10	3	Miscast	3
3761	2	10	3	Asignado mal un papel	3
3762	1	10	3	Misdeal	1
3763	2	10	3	Repartir mal	1
3764	1	10	3	Misdealt	2
3765	2	10	3	Repartió mal	2
3766	1	10	3	Misdealt	3
3767	2	10	3	Repartido mal	3
3768	1	10	3	Misgive	1
3769	2	10	3	Inspirar desconfianza	1
3770	1	10	3	Misgave	2
3771	2	10	3	Inspiró desconfianza	2
3772	1	10	3	Misgiven	3
3773	2	10	3	Inspirado desconfianza	3
3774	1	10	3	Mislay	1
3775	2	10	3	Extraviar	1
3776	1	10	3	Mislaid	2
3777	2	10	3	Extravió	2
3778	1	10	3	Mislaid	3
3779	2	10	3	Extraviado	3
3780	1	10	3	Mislead	1
3781	2	10	3	Desorientar	1
3782	1	10	3	Misled	2
3783	2	10	3	Desorientó	2
3784	1	10	3	Misled	3
3785	2	10	3	Desorientado	3
3786	1	10	3	Misread	1
3787	2	10	3	Leer mal	1
3788	1	10	3	Misread	2
3789	2	10	3	Leyó mal	2
3790	1	10	3	Misread	3
3791	2	10	3	Leído mal	3
3792	1	10	3	Misspeak	1
3793	2	10	3	Hablar mal	1
3794	1	10	3	Misspoke	2
3795	2	10	3	Habló mal	2
3796	1	10	3	Misspoken	3
3797	2	10	3	Hablado mal	3
3798	1	10	3	Misspell	1
3799	2	10	3	Deletrear mal	1
3800	1	10	3	Misspelt	2
3801	2	10	3	Deletreó mal	2
3802	1	10	3	Misspelt	3
3803	2	10	3	Deletreado mal	3
3804	1	10	3	Misspend	1
3805	2	10	3	Despilfarrar	1
3806	1	10	3	Misspent	2
3807	2	10	3	Despilfarró	2
3808	1	10	3	Misspent	3
3809	2	10	3	Despilfarrado	3
3810	1	10	3	Mistake	1
3811	2	10	3	Equivocarse	1
3812	1	10	3	Mistook	2
3813	2	10	3	Se equivocó	2
3814	1	10	3	Mistaken	3
3815	2	10	3	Equivocado	3
3816	1	10	3	Misunderstand	1
3817	2	10	3	Malentender	1
3818	1	10	3	Misunderstood	2
3819	2	10	3	Malentendió	2
3820	1	10	3	Misunderstood	3
3821	2	10	3	Malentendido	3
3822	1	10	3	Outbid	1
3823	2	10	3	Pujar más alto	1
3824	1	10	3	Outbid	2
3825	2	10	3	Pujó más alto	2
3826	1	10	3	Outbid	3
3827	2	10	3	Pujado más alto	3
3828	1	10	3	Outdo	1
3829	2	10	3	Superar	1
3830	1	10	3	Outdid	2
3831	2	10	3	Superó	2
3832	1	10	3	Outdone	3
3833	2	10	3	Superado	3
3834	1	10	3	Outgrow	1
3835	2	10	3	Quedar pequeño	1
3836	1	10	3	Outgrew	2
3837	2	10	3	Quedó pequeño	2
3838	1	10	3	Outgrown	3
3839	2	10	3	Quedado pequeño	3
3840	1	10	3	Outrun	1
3841	2	10	3	Correr más rápido	1
3842	1	10	3	Outran	2
3843	2	10	3	Corrió más rápido	2
3844	1	10	3	Outrun	3
3845	2	10	3	Corrido más rápido	3
3846	1	10	3	Outsell	1
3847	2	10	3	Vender más que	1
3848	1	10	3	Outsold	2
3849	2	10	3	Vendió más que	2
3850	1	10	3	Outsold	3
3851	2	10	3	Vendido más que	3
3852	1	10	3	Overcast	1
3853	2	10	3	Anublar	1
3854	1	10	3	Overcast	2
3855	2	10	3	Anubló	2
3856	1	10	3	Overcast	3
3857	2	10	3	Anublado	3
3858	1	10	3	Overdrive	1
3859	2	10	3	Sobrecargar	1
3860	1	10	3	Overdrove	2
3861	2	10	3	Sobrecargó	2
3862	1	10	3	Overdriven	3
3863	2	10	3	Sobrecargado	3
3864	1	10	3	Overfly	1
3865	2	10	3	Sobrevolar	1
3866	1	10	3	Overflew	2
3867	2	10	3	Sobrevoló	2
3868	1	10	3	Overflown	3
3869	2	10	3	Sobrevolado	3
3870	1	10	3	Overhang	1
3871	2	10	3	Pender sobre	1
3872	1	10	3	Overhung	2
3873	2	10	3	Pendió sobre	2
3874	1	10	3	Overhung	3
3875	2	10	3	Pendido sobre	3
3876	1	10	3	Overleap	1
3877	2	10	3	Saltar por encima	1
3878	1	10	3	Overleapt	2
3879	2	10	3	Saltó por encima	2
3880	1	10	3	Overleapt	3
3881	2	10	3	Saltado por encima	3
3882	1	10	3	Overlie	1
3883	2	10	3	Acostarse sobre	1
3884	1	10	3	Overlay	2
3885	2	10	3	Se acostó sobre	2
3886	1	10	3	Overlain	3
3887	2	10	3	Acostado sobre	3
3888	1	10	3	Overpay	1
3889	2	10	3	Pagar de más	1
3890	1	10	3	Overpaid	2
3891	2	10	3	Pagó de más	2
3892	1	10	3	Overpaid	3
3893	2	10	3	Pagado de más	3
3894	1	10	3	Override	1
3895	2	10	3	Anular	1
3896	1	10	3	Overrode	2
3897	2	10	3	Anuló	2
3898	1	10	3	Overridden	3
3899	2	10	3	Anulado	3
3900	1	10	3	Overrun	1
3901	2	10	3	Infestar	1
3902	1	10	3	Overran	2
3903	2	10	3	Infestó	2
3904	1	10	3	Overrun	3
3905	2	10	3	Infectado	3
3906	1	10	3	Oversee	1
3907	2	10	3	Supervisar	1
3908	1	10	3	Oversaw	2
3909	2	10	3	Supervisó	2
3910	1	10	3	Overseen	3
3911	2	10	3	Supervisado	3
3912	1	10	3	Overshoot	1
3913	2	10	3	Pasarse de largo	1
3914	1	10	3	Overshot	2
3915	2	10	3	Se pasó de largo	2
3916	1	10	3	Overshot	3
3917	2	10	3	Pasado de largo	3
3918	1	10	3	Oversleep	1
3919	2	10	3	Quedarse dormido	1
3920	1	10	3	Overslept	2
3921	2	10	3	Se quedó dormido	2
3922	1	10	3	Overslept	3
3923	2	10	3	Quedado dormido	3
3924	1	10	3	Overspend	1
3925	2	10	3	Gastar demasiado	1
3926	1	10	3	Overspent	2
3927	2	10	3	Gastó demasiado	2
3928	1	10	3	Overspent	3
3929	2	10	3	Gastado demasiado	3
3930	1	10	3	Overspread	1
3931	2	10	3	Cubrir la superficie	1
3932	1	10	3	Overspread	2
3933	2	10	3	Cubrió la superficie	2
3934	1	10	3	Overspread	3
3935	2	10	3	Cubierto la superficie	3
3936	1	10	3	Overtake	1
3937	2	10	3	Adelantar	1
3938	1	10	3	Overtook	2
3939	2	10	3	Adelantó	2
3940	1	10	3	Overtaken	3
3941	2	10	3	Adelantado	3
3942	1	10	3	Overthrow	1
3943	2	10	3	Derrocar	1
3944	1	10	3	Overthrew	2
3945	2	10	3	Derrocó	2
3946	1	10	3	Overthrown	3
3947	2	10	3	Derrocado	3
3948	1	10	3	Overwind	1
3949	2	10	3	Dar cuerda en exceso	1
3950	1	10	3	Overwound	2
3951	2	10	3	Dio cuerda en exceso	2
3952	1	10	3	Overwound	3
3953	2	10	3	Dado cuerda en exceso	3
3954	1	10	3	Overwrite	1
3955	2	10	3	Sobrescribir	1
3956	1	10	3	Overwrote	2
3957	2	10	3	Sobrescribió	2
3958	1	10	3	Overwritten	3
3959	2	10	3	Sobrescribito	3
\.


--
-- TOC entry 5132 (class 0 OID 24748)
-- Dependencies: 239
-- Data for Name: sesion_usuario; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.sesion_usuario (id, usuario_id, menu_actual, jugando, mod_j, ord_j, ayuda_juego, aciertos, fallos, c_idx, j_paso, j_status, j_indices, j_vistos, j_fallidos_json, fecha_guardado) FROM stdin;
\.


--
-- TOC entry 5119 (class 0 OID 16752)
-- Dependencies: 226
-- Data for Name: tipo_palabra; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tipo_palabra (id_tipo_palabra, tipo_palabra) FROM stdin;
1	Sustantivos
2	Adjetivos
3	Determinantes
4	Pronombres
6	Adverbios
7	Preposiciones
8	Conjunciones
9	Interjecciones
10	Verbos Irregulares
5	Verbos Regulares
\.


--
-- TOC entry 5117 (class 0 OID 16743)
-- Dependencies: 224
-- Data for Name: tipos_archivo; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tipos_archivo (id_tipo_archivo, tipo_archivo) FROM stdin;
1	Palabras
2	Verbos Compuestos
3	Modismos
\.


--
-- TOC entry 5130 (class 0 OID 24721)
-- Dependencies: 237
-- Data for Name: usuarios; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.usuarios (id_usuario, nombre, correo, alias, nivel, clave, token_verificacion, fecha_registro, ultimo_cambio_pwd, estado, intentos_fallidos, es_admin) FROM stdin;
1	Edwin Reyes	edwinreyes308@gmail.com	EdwinReyes	Intermedio	peluche_27	\N	2026-05-11 21:28:24.393832	2026-05-11 21:28:24.393832	ACTIVO	0	f
3	Maria Elvira Perez de Reyes	mariaelviraperezcardenas@gmail.com	peluche	Básico	peluche*08	\N	2026-05-11 22:25:44.182985	2026-05-11 22:25:44.182985	ACTIVO	0	f
\.


--
-- TOC entry 5128 (class 0 OID 24621)
-- Dependencies: 235
-- Data for Name: verbos_compuestos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.verbos_compuestos (id_verbo, id_lenguaje, id_nivel, verbo) FROM stdin;
1	1	1	Ask for
1	2	1	Pedir
2	1	1	Back up
2	2	1	Apoyar / Respaldar
3	1	1	Blow up
3	2	1	Explotar
4	1	1	Break down
4	2	1	Averiarse / Romperse
5	1	1	Break up
5	2	1	Terminar una relación
6	1	1	Bring up
6	2	1	Mencionar / Criar
7	1	1	Call back
7	2	1	Devolver una llamada
8	1	1	Call off
8	2	1	Cancelar
9	1	1	Carry on
9	2	1	Continuar
10	1	1	Carry out
10	2	1	Llevar a cabo
11	1	1	Check in
11	2	1	Registrarse
12	1	1	Check out
12	2	1	Pagar y salir / Investigar
13	1	1	Clean up
13	2	1	Limpiar
14	1	1	Come back
14	2	1	Regresar
15	1	1	Come in
15	2	1	Entrar
16	1	1	Come on
16	2	1	¡Vamos! / Darse prisa
17	1	1	Cut down
17	2	1	Reducir
18	1	1	Cut off
18	2	1	Cortar / Interrumpir
19	1	1	Dress up
19	2	1	Disfrazarse / Vestirse elegante
20	1	1	Drop off
20	2	1	Dejar a alguien o algo
21	1	1	Eat out
21	2	1	Comer fuera
22	1	1	End up
22	2	1	Terminar / Acabar
23	1	1	Fall down
23	2	1	Caerse
24	1	1	Fill in
24	2	1	Rellenar (un formulario)
25	1	1	Fill up
25	2	1	Llenar por completo
26	1	1	Find out
26	2	1	Descubrir / Enterarse
27	1	1	Get along
27	2	1	Llevarse bien
28	1	1	Get away
28	2	1	Escapar
29	1	1	Get back
29	2	1	Volver / Recuperar
30	1	1	Get in
30	2	1	Entrar (a un coche)
31	1	1	Get off
31	2	1	Bajarse (de un bus/tren)
32	1	1	Get on
32	2	1	Subirse / Llevarse
33	1	1	Get out
33	2	1	Salir
34	1	1	Get up
34	2	1	Levantarse
35	1	1	Give away
35	2	1	Regalar / Revelar
36	1	1	Give back
36	2	1	Devolver
37	1	1	Give up
37	2	1	Rendirse / Dejar un hábito
38	1	1	Go away
38	2	1	Irse
39	1	1	Go back
39	2	1	Volver
40	1	1	Go on
40	2	1	Continuar / Pasar
41	1	1	Go out
41	2	1	Salir (de fiesta/paseo)
42	1	1	Go up
42	2	1	Subir / Aumentar
43	1	1	Grow up
43	2	1	Crecer / Hacerse adulto
44	1	1	Hang on
44	2	1	Esperar un momento
45	1	1	Hang up
45	2	1	Colgar (el teléfono)
46	1	1	Hold on
46	2	1	Esperar / Aguantar
47	1	1	Hurry up
47	2	1	Darse prisa
48	1	1	Keep on
48	2	1	Seguir haciendo algo
49	1	1	Keep up
49	2	1	Mantener el ritmo
50	1	1	Let in
50	2	1	Dejar entrar
51	1	1	Look after
51	2	1	Cuidar a
52	1	1	Look for
52	2	1	Buscar
53	1	1	Look forward to
53	2	1	Anhelar / Tener ganas
54	1	1	Look out
54	2	1	Tener cuidado
55	1	1	Look up
55	2	1	Buscar (en un libro/lista)
56	1	1	Make up
56	2	1	Inventar / Reconciliarse
57	1	1	Move in
57	2	1	Mudarse (a un lugar)
58	1	1	Move out
58	2	1	Mudarse (irse de un lugar)
59	1	1	Pay back
59	2	1	Devolver dinero
60	1	1	Pick up
60	2	1	Recoger / Levantar
61	1	1	Point out
61	2	1	Señalar / Indicar
62	1	1	Put away
62	2	1	Guardar en su sitio
63	1	1	Put off
63	2	1	Posponer
64	1	1	Put on
64	2	1	Ponerse (ropa/música)
65	1	1	Put out
65	2	1	Extinguir / Apagar fuego
66	1	1	Run away
66	2	1	Huir
67	1	1	Run out of
67	2	1	Quedarse sin algo
68	1	1	Set up
68	2	1	Configurar / Instalar
69	1	1	Show up
69	2	1	Aparecer / Llegar
70	1	1	Sit down
70	2	1	Sentarse
71	1	1	Stand up
71	2	1	Ponerse de pie
72	1	1	Switch off
72	2	1	Apagar
73	1	1	Switch on
73	2	1	Encender
74	1	1	Take after
74	2	1	Parecerse a
75	1	1	Take away
75	2	1	Llevarse / Quitar
76	1	1	Take off
76	2	1	Quitarse (ropa) / Despegar
77	1	1	Take out
77	2	1	Sacar
78	1	1	Talk about
78	2	1	Hablar sobre
79	1	1	Throw away
79	2	1	Tirar a la basura
80	1	1	Try on
80	2	1	Probarse (ropa)
81	1	1	Try out
81	2	1	Probar algo nuevo
82	1	1	Turn down
82	2	1	Bajar volumen / Rechazar
83	1	1	Turn off
83	2	1	Apagar
84	1	1	Turn on
84	2	1	Encender
85	1	1	Turn up
85	2	1	Subir volumen / Aparecer
86	1	1	Wake up
86	2	1	Despertarse
87	1	1	Warm up
87	2	1	Calentar
88	1	1	Watch out
88	2	1	Tener cuidado
89	1	1	Work out
89	2	1	Hacer ejercicio / Resolver
90	1	1	Write down
90	2	1	Anotar
91	1	1	Break into
91	2	1	Entrar a la fuerza
92	1	1	Call on
92	2	1	Visitar / Recurrir a
93	1	1	Check out
93	2	1	Echar un vistazo
94	1	1	Come across
94	2	1	Encontrarse con algo
95	1	1	Cut in
95	2	1	Interrumpir
96	1	1	Drop in
96	2	1	Pasar a visitar
97	1	1	Get by
97	2	1	Arreglárselas
98	1	1	Give in
98	2	1	Ceder
99	1	1	Look into
99	2	1	Investigar
100	1	1	Set off
100	2	1	Partir / Salir de viaje
201	1	1	Abide by
202	2	1	Cumplir con / Acatar
203	1	1	Add up
204	2	1	Cuadrar / Tener sentido
205	1	1	Allow for
206	2	1	Tener en cuenta / Prever
207	1	1	Bank on
208	2	1	Confiar en / Contar con
209	1	1	Blast off
210	2	1	Despegar (cohete)
211	1	1	Bottle up
212	2	1	Reprimir (emociones)
213	1	1	Branch out
214	2	1	Expandirse / Diversificarse
215	1	1	Breeze through
216	2	1	Hacer algo con facilidad
217	1	1	Buckle up
218	2	1	Abrocharse el cinturón
219	1	1	Bundle up
220	2	1	Abrigarse mucho
221	1	1	Burst in
222	2	1	Irrumpir
223	1	1	Carry over
224	2	1	Traspasar / Aplazar
225	1	1	Cash in
226	2	1	Sacar provecho / Cobrar
227	1	1	Chance upon
228	2	1	Encontrarse por casualidad
229	1	1	Clear out
230	2	1	Desalojar / Vaciar
231	1	1	Conjure up
232	2	1	Evocar / Imaginar
233	1	1	Cope with
234	2	1	Sobrellevar / Lidiar con
235	1	1	Crop up
236	2	1	Surgir de repente
237	1	1	Die out
238	2	1	Extinguirse
239	1	1	Doze off
240	2	1	Quedarse dormido
241	1	1	Dwell on
242	2	1	Darle vueltas a algo
243	1	1	Eavesdrop on
244	2	1	Escuchar a escondidas
245	1	1	Embark on
246	2	1	Embarcarse en / Iniciar
247	1	1	Fathom out
248	2	1	Llegar a comprender
249	1	1	Fend off
250	2	1	Rechazar / Esquivar
251	1	1	Flare up
252	2	1	Estallar / Agravarse
253	1	1	Follow through
254	2	1	Llevar a término
255	1	1	Frown upon
256	2	1	Ver con malos ojos
257	1	1	Gear up
258	2	1	Prepararse / Equiparse
259	1	1	Gloss over
260	2	1	Pasar por alto / Minimizar
261	1	1	Hammer out
262	2	1	Llegar a un acuerdo difícil
263	1	1	Hinge on
264	2	1	Depender de
265	1	1	Iron out
266	2	1	Resolver / Limar asperezas
267	1	1	Jot down
268	2	1	Anotar rápidamente
269	1	1	Key in
270	2	1	Teclear / Introducir datos
271	1	1	Lash out
272	2	1	Arremeter / Atacar
273	1	1	Lay off
274	2	1	Despedir (del trabajo)
275	1	1	Leap at
276	2	1	Aprovechar (una oportunidad)
277	1	1	Level off
278	2	1	Estabilizarse
279	1	1	Live up to
280	2	1	Estar a la altura de
281	1	1	Log off
282	2	1	Cerrar sesión
283	1	1	Log on
284	2	1	Iniciar sesión
285	1	1	Measure up
286	2	1	Dar la talla
287	1	1	Mull over
288	2	1	Reflexionar / Meditar
289	1	1	Narrow down
290	2	1	Reducir opciones
291	1	1	Nod off
292	2	1	Dar cabezadas (sueño)
293	1	1	Own up
294	2	1	Confesar / Admitir
295	1	1	Phase out
296	2	1	Retirar gradualmente
297	1	1	Pitch in
298	2	1	Colaborar / Arrimar el hombro
299	1	1	Rule out
300	2	1	Descartar
301	1	2	Back out
302	2	2	Retirarse / Echarse atrás
303	1	2	Bear with
304	2	2	Tener paciencia con
305	1	2	Blow out
306	2	2	Apagar (soplando) / Reventar
307	1	2	Break away
308	2	2	Soltarse / Desprenderse
309	1	2	Bring about
310	2	2	Provocar / Ocasionar
311	1	2	Brush up on
312	2	2	Repasar / Refrescar conocimientos
313	1	2	Burn out
314	2	2	Consumirse / Agotarse (estrés)
315	1	2	Call forth
316	2	2	Provocar / Evocar
317	1	2	Calm down
318	2	2	Calmarse
319	1	2	Check up on
320	2	2	Vigilar / Controlar a alguien
321	1	2	Cheer up
322	2	2	Alegrar / Animarse
323	1	2	Chop up
324	2	2	Trocear / Picar
325	1	2	Close down
326	2	2	Cerrar permanentemente
327	1	2	Come along
328	2	2	Acompañar / Progresar
329	1	2	Come down with
330	2	2	Enfermar de
331	1	2	Count on
332	2	2	Contar con (alguien)
333	1	2	Crack down on
334	2	2	Tomar medidas severas contra
335	1	2	Cut out
336	2	2	Recortar / Dejar de hacer algo
337	1	2	Dash off
338	2	2	Hacer algo de prisa / Salir corriendo
339	1	2	Deal with
340	2	2	Tratar con / Encargarse de
341	1	2	Dig into
342	2	2	Investigar a fondo
343	1	2	Dish out
344	2	2	Repartir / Dar
345	1	2	Draw up
346	2	2	Redactar / Preparar (documento)
347	1	2	Dream up
348	2	2	Imaginar / Inventar
349	1	2	Drive away
350	2	2	Ahuyentar / Irse en coche
351	1	2	Drop out
352	2	2	Abandonar (estudios/carrera)
353	1	2	Dry up
354	2	2	Secarse / Quedarse sin palabras
355	1	2	Face up to
356	2	2	Afrontar / Dar la cara
357	1	2	Fall apart
358	2	2	Desmoronarse / Hacerse pedazos
359	1	2	Fall through
360	2	2	Fracasar (planes/proyectos)
361	1	2	Feel up to
362	2	2	Sentirse con ánimos para
363	1	2	Fight back
364	2	2	Defenderse / Contraatacar
365	1	2	Figure out
366	2	2	Comprender / Resolver
367	1	2	Fill out
368	2	2	Completar (un formulario)
369	1	2	Fit in
370	2	2	Encajar / Adaptarse
371	1	2	Focus on
372	2	2	Concentrarse en
373	1	2	Get across
374	2	2	Hacerse entender / Comunicar
375	1	2	Get ahead
376	2	2	Progresar / Salir adelante
377	1	2	Get around
378	2	2	Esquivar (problema) / Desplazarse
379	1	2	Get at
380	2	2	Insinuar / Alcanzar
381	1	2	Get down
382	2	2	Deprimir / Agacharse
383	1	2	Get down to
384	2	2	Ponerse manos a la obra
385	1	2	Get over
386	2	2	Superar / Recuperarse de
387	1	2	Get through
388	2	2	Terminar algo / Lograr contactar
389	1	2	Give off
390	2	2	Desprender (olor/luz)
391	1	2	Go ahead
392	2	2	Seguir adelante / Dar permiso
393	1	2	Go by
394	2	2	Pasar (el tiempo) / Guiarse por
395	1	2	Go for
396	2	2	Atacar / Intentar conseguir algo
397	1	2	Go over
398	2	2	Revisar / Repasar
399	1	2	Go through
400	2	2	Sufrir / Examinar detalladamente
401	1	2	Go without
402	2	2	Pasar sin algo / Privarse de
403	1	2	Hand in
404	2	2	Entregar (tarea/informe)
405	1	2	Hand out
406	2	2	Distribuir / Repartir
407	1	2	Hang out
408	2	2	Pasar el rato / Pasar tiempo con
409	1	2	Head for
410	2	2	Dirigirse hacia
411	1	2	Hear from
412	2	2	Tener noticias de alguien
413	1	2	Help out
414	2	2	Echar una mano
415	1	2	Hold back
416	2	2	Contener / Frenar
417	1	2	Hold up
418	2	2	Retrasar / Atracar
419	1	2	Keep away
420	2	2	Mantener alejado
421	1	2	Keep off
422	2	2	No pisar / Mantenerse fuera
423	1	2	Keep out
424	2	2	Prohibir la entrada
425	1	2	Knock down
426	2	2	Derribar / Atropellar
427	1	2	Knock out
428	2	2	Dejar inconsciente / Noquear
429	1	2	Lay down
430	2	2	Establecer (reglas) / Dejar en el suelo
431	1	2	Lead to
432	2	2	Conducir a / Provocar
432	1	2	Leave behind
434	2	2	Olvidar / Dejar atrás
435	1	2	Leave out
436	2	2	Excluir / Omitir
437	1	2	Let down
438	2	2	Decepcionar
439	1	2	Let out
440	2	2	Dejar salir / Soltar
441	1	2	Line up
442	2	2	Hacer cola / Alinear
443	1	2	Listen to
444	2	2	Escuchar a
445	1	2	Live on
446	2	2	Vivir de / Alimentarse de
447	1	2	Look down on
448	2	2	Despreciar / Mirar por encima del hombro
449	1	2	Look forward
450	2	2	Mirar hacia adelante
451	1	2	Luck out
452	2	2	Tener mucha suerte
453	1	2	Make for
454	2	2	Dirigirse hacia / Contribuir a
455	1	2	Make out
456	2	2	Distinguir / Entender algo difícil
457	1	2	Make up for
458	2	2	Compensar por
459	1	2	Mess up
460	2	2	Arruinar / Cometer un error
461	1	2	Mix up
462	2	2	Confundir / Mezclar
463	1	2	Open up
464	2	2	Sincerarse / Abrir (negocio)
465	1	2	Opt out
466	2	2	Decidir no participar
467	1	2	Pass away
468	2	2	Fallecer
469	1	2	Pass out
470	2	2	Desmayarse
471	1	2	Pick on
472	2	2	Meterse con alguien / Molestar
473	1	2	Plug in
474	2	2	Enchufar
475	1	2	Pull over
476	2	2	Orillarse con el coche
477	1	2	Pull through
478	2	2	Sobrevivir / Salir de una enfermedad
479	1	2	Put back
480	2	2	Poner en su sitio / Retrasar
481	1	2	Put up with
482	2	2	Tolerar / Aguantar
483	1	2	Read over
484	2	2	Leer detenidamente
485	1	2	Rely on
486	2	2	Confiar en / Depender de
487	1	2	Remind of
488	2	2	Recordar a algo o alguien
489	1	2	Ring up
490	2	2	Llamar por teléfono / Marcar en caja
491	1	2	Rip off
492	2	2	Estafar / Timar
493	1	2	Rule out
494	2	2	Descartar / Excluir
495	1	2	Run into
496	2	2	Encontrarse con alguien de casualidad
497	1	2	Run over
498	2	2	Atropellar / Repasar rápido
499	1	2	Save up
500	2	2	Ahorrar
501	1	2	See off
502	2	2	Despedir a alguien (en viaje)
503	1	2	See through
504	2	2	Ver las intenciones de / Llevar a cabo
505	1	2	Sell out
506	2	2	Agotarse las existencias
507	1	2	Send back
508	2	2	Devolver
509	1	2	Settle down
510	2	2	Establecerse / Calmarse
511	1	2	Settle for
512	2	2	Conformarse con
513	1	2	Shake up
514	2	2	Sacudir / Conmocionar
515	1	2	Show off
516	2	2	Presumir / Alardear
517	1	2	Shut down
518	2	2	Apagar (maquinaria) / Cerrar
519	1	2	Shut up
520	2	2	Callarse
521	1	2	Sign in
522	2	2	Registrar entrada
523	1	2	Sign out
524	2	2	Registrar salida
525	1	2	Sign up
526	2	2	Inscribirse / Apuntarse
527	1	2	Sink in
528	2	2	Ser asimilado (idea o noticia)
529	1	2	Sleep on
530	2	2	Consultar con la almohada
531	1	2	Slip up
532	2	2	Cometer un desliz / Error
533	1	2	Slow down
534	2	2	Ir más despacio
535	1	2	Sort out
536	2	2	Solucionar / Ordenar
537	1	2	Speak up
538	2	2	Hablar más alto / Expresarse
539	1	2	Split up
540	2	2	Separarse / Dividirse
541	1	2	Stand by
542	2	2	Apoyar / Estar a la espera
543	1	2	Stand for
544	2	2	Significar / Tolerar
545	1	2	Stand out
546	2	2	Destacar / Sobresalir
547	1	2	Stay up
548	2	2	Quedarse despierto
549	1	2	Stick to
550	2	2	Ceñirse a / Mantenerse fiel
551	1	2	Take back
552	2	2	Retractarse / Devolver
553	1	2	Take in
554	2	2	Engañar / Asimilar información
555	1	2	Take on
556	2	2	Asumir (reto/empleado) / Enfrentarse
557	1	2	Take over
558	2	2	Tomar el control
559	1	2	Take up
560	2	2	Empezar (hábito/afición) / Ocupar espacio
561	1	2	Tell off
562	2	2	Rañar / Regañar
563	1	2	Think over
564	2	2	Reflexionar
565	1	2	Think up
566	2	2	Idear / Inventar
567	1	2	Throw up
568	2	2	Vomitar
569	1	2	Tidy up
570	2	2	Ordenar / Limpiar un poco
571	1	2	Touch on
572	2	2	Mencionar brevemente
573	1	2	Track down
574	2	2	Rastrear / Localizar
575	1	2	Turn away
576	2	2	Rechazar / No dejar entrar
577	1	2	Turn into
578	2	2	Convertirse en
579	1	2	Turn out
580	2	2	Resultar ser / Apagar (luz)
581	1	2	Use up
582	2	2	Gastar / Consumir todo
583	1	2	Wait for
584	2	2	Esperar a
585	1	2	Wait on
586	2	2	Atender (en mesa) / Servir
587	1	2	Walk out
588	2	2	Abandonar (lugar/huelga)
589	1	2	Wash up
590	2	2	Lavar los platos
591	1	2	Wear off
592	2	2	Pasarse el efecto
593	1	2	Wear out
594	2	2	Desgastar / Dejar exhausto
595	1	2	Wipe out
596	2	2	Aniquilar / Limpiar por completo
597	1	2	Write off
598	2	2	Dar por perdido / Cancelar deuda
599	1	2	Yield to
600	2	2	Ceder ante
601	1	3	Alight on
602	2	3	Notar / Encontrar por casualidad
603	1	3	Answer for
604	2	3	Responsabilizarse de
605	1	3	Argue out
606	2	3	Debatir hasta llegar a una conclusión
607	1	3	Auction off
608	2	3	Subastar
609	1	3	Avenge on
610	2	3	Vengarse de
611	1	3	Bail out
612	2	3	Rescatar financieramente
613	1	3	Bargain for
614	2	3	Esperar / Contar con algo
615	1	3	Beaver away
616	2	3	Trabajar duro y con constancia
617	1	3	Beef up
618	2	3	Reforzar / Fortalecer
619	1	3	Belt out
620	2	3	Cantar a todo pulmón
621	1	3	Blare out
622	2	3	Resonar estruendosamente
623	1	3	Blot out
624	2	3	Borrar de la memoria / Tapar (luz)
625	1	3	Blunder upon
626	2	3	Encontrar por error o torpeza
627	1	3	Board up
628	2	3	Cerrar con tablas
629	1	3	Bone up on
630	2	3	Empollar / Estudiar mucho un tema
631	1	3	Botch up
632	2	3	Arruinar / Hacer una chapuza
633	1	3	Bow out
634	2	3	Retirarse discretamente
635	1	3	Box in
636	2	3	Acorralar / Encerrar
637	1	3	Bridle at
638	2	3	Ofenderse / Indignarse
639	1	3	Brim over
640	2	3	Desbordarse (emociones)
641	1	3	Buck up
642	2	3	Animarse / Darse prisa
643	1	3	Buoy up
644	2	3	Mantener a flote / Dar ánimos
645	1	3	Buy off
646	2	3	Sobornar
647	1	3	Call down
648	2	3	Regañar severamente
649	1	3	Cast aside
650	2	3	Desechar / Dejar de lado
651	1	3	Cave in
652	2	3	Ceder / Desmoronarse
653	1	3	Chalk up to
654	2	3	Atribuir a
655	1	3	Chime in
656	2	3	Intervenir en una conversación
657	1	3	Clamp down on
658	2	3	Reprimir severamente
659	1	3	Claw back
660	2	3	Recuperar con esfuerzo
661	1	3	Clutter up
662	2	3	Abarrotar / Desordenar
663	1	3	Cotton on
664	2	3	Darse cuenta / Captar la idea
665	1	3	Cough up
666	2	3	Soltar (dinero o información) a regañadientes
667	1	3	Crush out
668	2	3	Extinguir / Aplastar
669	1	3	Cry out for
670	2	3	Pedir a gritos (necesidad)
671	1	3	Damp down
672	2	3	Apaciguar / Sofocar
673	1	3	Descend on
674	2	3	Caer de improviso
675	1	3	Dig up
676	2	3	Desenterrar / Investigar pasado
677	1	3	Dole out
678	2	3	Repartir con parsimonia
679	1	3	Dragoon into
680	2	3	Coaccionar / Obligar
681	1	3	Drain away
682	2	3	Escurrir / Desaparecer poco a poco
683	1	3	Draw out
684	2	3	Prolongar / Hacer hablar a alguien
685	1	3	Dredge up
686	2	3	Sacar a relucir algo desagradable
687	1	3	Drift apart
688	2	3	Distanciarse emocionalmente
689	1	3	Drum up
690	2	3	Fomentar / Conseguir apoyo
691	1	3	Egg on
692	2	3	Incitar / Azuzar
693	1	3	Eke out
694	2	3	Hacer que algo dure / Sobrevivir con poco
695	1	3	Explain away
696	2	3	Justificar / Dar una excusa para algo malo
697	1	3	Face down
698	2	3	Enfrentar con firmeza
699	1	3	Fall back on
700	2	3	Recurrir a algo en última instancia
701	1	3	Farm out
702	2	3	Subcontratar / Delegar
703	1	3	Ferret out
704	2	3	Husmear / Localizar información oculta
705	1	3	Finish off
706	2	3	Aniquilar / Terminar por completo
707	1	3	Fish for
708	2	3	Pescar (cumplidos/información)
709	1	3	Fitter away
710	2	3	Desperdiciar / Malgastar
711	1	3	Flesh out
712	2	3	Dar cuerpo / Desarrollar una idea
713	1	3	Flog to death
714	2	3	Abusar de un tema hasta aburrir
715	1	3	Fork out
716	2	3	Pagar a regañadientes
717	1	3	Gain on
718	2	3	Ganar terreno / Acercarse
719	1	3	Get at
720	2	3	Insinuar / Criticar
721	1	3	Gloss over
722	2	3	Minimizar un error / Pasar por alto
723	1	3	Go along with
724	2	3	Estar de acuerdo con
725	1	3	Go for broke
726	2	3	Jugárselo todo
727	1	3	Grovel to
728	2	3	Humillarse ante alguien
729	1	3	Hack away at
730	2	3	Talar / Reducir con esfuerzo
731	1	3	Hark back to
732	2	3	Evocar algo del pasado
733	1	3	Have it out with
734	2	3	Aclarar las cosas con alguien
735	1	3	Heap up
736	2	3	Amontonar
737	1	3	Hem in
738	2	3	Cercar / Limitar movimientos
739	1	3	Hold forth on
740	2	3	Hablar extensamente sobre
741	1	3	Hone in on
742	2	3	Dirigirse directamente a
743	1	3	Hush up
744	2	3	Ocultar un escándalo / Silenciar
745	1	3	Ice over
746	2	3	Congelarse la superficie
747	1	3	Idle away
748	2	3	Perder el tiempo
749	1	3	Impinge on
750	2	3	Afectar negativamente / Incidir
751	1	3	Inquire into
752	2	3	Investigar formalmente
753	1	3	Jack up
754	2	3	Subir precios / Levantar con gato
755	1	3	Jaw away
756	2	3	Hablar sin parar
757	1	3	Jump at
758	2	3	Aceptar de inmediato
759	1	3	Keel over
760	2	3	Desmayarse / Volcarse
761	1	3	Keep in with
762	2	3	Mantenerse en buenos términos con
763	1	3	Kick in
764	2	3	Empezar a surtir efecto
765	1	3	Knuckle down
766	2	3	Ponerse a trabajar seriamente
767	1	3	Lap up
768	2	3	Disfrutar algo con avidez
769	1	3	Lay into
770	2	3	Atacar verbalmente
771	1	3	Lead off
772	2	3	Comenzar / Dar el primer paso
773	1	3	Leaf through
774	2	3	Hojear rápido
775	1	3	Lean on
776	2	3	Presionar a alguien / Apoyarse
777	1	3	Let on
778	2	3	Revelar un secreto
779	1	3	Level with
780	2	3	Ser franco con alguien
781	1	3	Live down
782	2	3	Hacer olvidar un error pasado
783	1	3	Look on
784	2	3	Observar sin participar
785	1	3	Lord it over
786	2	3	Tratar a otros con superioridad
787	1	3	Make away with
788	2	3	Escapar con un botín
789	1	3	Make off with
790	2	3	Robar y huir
791	1	3	Map out
792	2	3	Planificar detalladamente
793	1	3	Mark down
794	2	3	Rebajar precio / Bajar nota
795	1	3	Measure out
796	2	3	Dosificar / Medir
797	1	3	Melt away
798	2	3	Esfumarse / Desvanecerse
799	1	3	Met out
800	2	3	Infligir / Imponer castigo
801	1	3	Muck up
802	2	3	Echar a perder
803	1	3	Muscle in on
804	2	3	Entrometerse a la fuerza
805	1	3	Niggle at
806	2	3	Preocupar / Molestar constantemente
807	1	3	Nose about
808	2	3	Husmear
809	1	3	Note down
810	2	3	Tomar nota
811	1	3	Occur to
812	2	3	Venirse a la mente
813	1	3	Open onto
814	2	3	Dar a (una vista o lugar)
815	1	3	Own up to
816	2	3	Confesar algo malo
817	1	3	Pack in
818	2	3	Abandonar algo / Meter a presión
819	1	3	Pal around with
820	2	3	Andar con amigos
821	1	3	Palm off on
822	2	3	Endosar algo falso o malo
823	1	3	Pan out
824	2	3	Salir bien / Dar resultado
825	1	3	Part with
826	2	3	Desprenderse de algo querido
827	1	3	Patch up
828	2	3	Remendar / Reconciliarse
829	1	3	Pay off
830	2	3	Valer la pena / Liquidar deuda
831	1	3	Peg out
832	2	3	Estirar la pata (morir) / Agotarse
833	1	3	Peter out
834	2	3	Agotarse gradualmente
835	1	3	Pick apart
836	2	3	Analizar críticamente
837	1	3	Pig out
838	2	3	Atiborrarse de comida
839	1	3	Pile up
840	2	3	Acumularse
841	1	3	Pin down
842	2	3	Definir con precisión / Inmovilizar
843	1	3	Pine for
844	2	3	Añorar intensamente
845	1	3	Pipe down
846	2	3	Callarse (imperativo)
847	1	3	Play down
848	2	3	Restar importancia
849	1	3	Plough into
850	2	3	Estrellarse contra / Invertir en
851	1	3	Pluck up
852	2	3	Armarse de (valor)
853	1	3	Polish off
854	2	3	Acabar rápido (comida o tarea)
855	1	3	Pore over
856	2	3	Estudiar con mucha atención
857	1	3	Pull off
858	2	3	Lograr algo difícil
859	1	3	Push for
860	2	3	Presionar para conseguir algo
861	1	3	Put across
862	2	3	Comunicar eficazmente
863	1	3	Put upon
864	2	3	Abusar de la confianza de alguien
865	1	3	Quiet down
866	2	3	Hacer silencio
867	1	3	Rake in
868	2	3	Ganar dinero a espuertas
869	1	3	Rattle off
870	2	3	Recitar de memoria rápidamente
871	1	3	Read into
872	2	3	Ver segundas intenciones
873	1	3	Reckon on
874	2	3	Contar con algo
875	1	3	Reel off
876	2	3	Decir de corrido
877	1	3	Rein in
878	2	3	Frenar / Controlar
879	1	3	Rough out
880	2	3	Hacer un bosquejo
881	1	3	Round off
882	2	3	Redondear / Culminar bien
883	1	3	Rub in
884	2	3	Recordar algo desagradable (regañar)
885	1	3	Run up against
886	2	3	Tropezar con (dificultades)
887	1	3	Scrape by
888	2	3	Pasar con lo justo
889	1	3	Screw up
890	2	3	Fastidiarla / Arruinar
891	1	3	Set about
892	2	3	Ponerse a hacer algo
893	1	3	Shrug off
894	2	3	Restar importancia / Desestimar
895	1	3	Single out
896	2	3	Seleccionar / Señalar
897	1	3	Size up
898	2	3	Evaluar / Tantear
899	1	3	Skimp on
900	2	3	Escatimar en
\.


--
-- TOC entry 5147 (class 0 OID 0)
-- Dependencies: 227
-- Name: diccionario_base_id_diccionario_base_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.diccionario_base_id_diccionario_base_seq', 1, false);


--
-- TOC entry 5148 (class 0 OID 0)
-- Dependencies: 229
-- Name: diccionario_uso_id_registro_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.diccionario_uso_id_registro_seq', 1, false);


--
-- TOC entry 5149 (class 0 OID 0)
-- Dependencies: 219
-- Name: lenguajes_id_lenguaje_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.lenguajes_id_lenguaje_seq', 1, false);


--
-- TOC entry 5150 (class 0 OID 0)
-- Dependencies: 221
-- Name: nivel_id_nivel_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.nivel_id_nivel_seq', 1, false);


--
-- TOC entry 5151 (class 0 OID 0)
-- Dependencies: 231
-- Name: paises_id_pais_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.paises_id_pais_seq', 1, false);


--
-- TOC entry 5152 (class 0 OID 0)
-- Dependencies: 238
-- Name: sesion_usuario_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.sesion_usuario_id_seq', 1, false);


--
-- TOC entry 5153 (class 0 OID 0)
-- Dependencies: 225
-- Name: tipo_palabra_id_tipo_palabra_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tipo_palabra_id_tipo_palabra_seq', 10, true);


--
-- TOC entry 5154 (class 0 OID 0)
-- Dependencies: 223
-- Name: tipos_archivo_id_tipo_archivo_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tipos_archivo_id_tipo_archivo_seq', 1, false);


--
-- TOC entry 5155 (class 0 OID 0)
-- Dependencies: 236
-- Name: usuarios_id_usuario_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.usuarios_id_usuario_seq', 3, true);


--
-- TOC entry 4938 (class 2606 OID 16831)
-- Name: diccionario_base diccionario_base_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.diccionario_base
    ADD CONSTRAINT diccionario_base_pkey PRIMARY KEY (id_diccionario_base);


--
-- TOC entry 4940 (class 2606 OID 16864)
-- Name: diccionario_uso diccionario_uso_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.diccionario_uso
    ADD CONSTRAINT diccionario_uso_pkey PRIMARY KEY (id_registro);


--
-- TOC entry 4930 (class 2606 OID 16732)
-- Name: lenguajes lenguajes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.lenguajes
    ADD CONSTRAINT lenguajes_pkey PRIMARY KEY (id_lenguaje);


--
-- TOC entry 4946 (class 2606 OID 24619)
-- Name: modismos modismos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.modismos
    ADD CONSTRAINT modismos_pkey PRIMARY KEY (id_modismo, id_lenguaje);


--
-- TOC entry 4932 (class 2606 OID 16741)
-- Name: nivel nivel_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.nivel
    ADD CONSTRAINT nivel_pkey PRIMARY KEY (id_nivel);


--
-- TOC entry 4942 (class 2606 OID 24588)
-- Name: paises paises_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.paises
    ADD CONSTRAINT paises_pkey PRIMARY KEY (id_pais);


--
-- TOC entry 4944 (class 2606 OID 24610)
-- Name: palabras palabras_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.palabras
    ADD CONSTRAINT palabras_pkey PRIMARY KEY (id_palabra, id_lenguaje);


--
-- TOC entry 4958 (class 2606 OID 24764)
-- Name: sesion_usuario sesion_usuario_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sesion_usuario
    ADD CONSTRAINT sesion_usuario_pkey PRIMARY KEY (id);


--
-- TOC entry 4936 (class 2606 OID 16759)
-- Name: tipo_palabra tipo_palabra_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tipo_palabra
    ADD CONSTRAINT tipo_palabra_pkey PRIMARY KEY (id_tipo_palabra);


--
-- TOC entry 4934 (class 2606 OID 16750)
-- Name: tipos_archivo tipos_archivo_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tipos_archivo
    ADD CONSTRAINT tipos_archivo_pkey PRIMARY KEY (id_tipo_archivo);


--
-- TOC entry 4950 (class 2606 OID 24742)
-- Name: usuarios usuarios_alias_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_alias_key UNIQUE (alias);


--
-- TOC entry 4952 (class 2606 OID 24740)
-- Name: usuarios usuarios_correo_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_correo_key UNIQUE (correo);


--
-- TOC entry 4954 (class 2606 OID 24744)
-- Name: usuarios usuarios_nivel_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_nivel_key UNIQUE (nivel);


--
-- TOC entry 4956 (class 2606 OID 24738)
-- Name: usuarios usuarios_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_pkey PRIMARY KEY (id_usuario);


--
-- TOC entry 4948 (class 2606 OID 24629)
-- Name: verbos_compuestos verbos_compuestos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.verbos_compuestos
    ADD CONSTRAINT verbos_compuestos_pkey PRIMARY KEY (id_verbo, id_lenguaje);


--
-- TOC entry 4959 (class 2606 OID 16842)
-- Name: diccionario_base diccionario_base_id_lenguaje_1_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.diccionario_base
    ADD CONSTRAINT diccionario_base_id_lenguaje_1_fkey FOREIGN KEY (id_lenguaje_1) REFERENCES public.lenguajes(id_lenguaje);


--
-- TOC entry 4960 (class 2606 OID 16847)
-- Name: diccionario_base diccionario_base_id_lenguaje_2_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.diccionario_base
    ADD CONSTRAINT diccionario_base_id_lenguaje_2_fkey FOREIGN KEY (id_lenguaje_2) REFERENCES public.lenguajes(id_lenguaje);


--
-- TOC entry 4961 (class 2606 OID 16837)
-- Name: diccionario_base diccionario_base_id_nivel_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.diccionario_base
    ADD CONSTRAINT diccionario_base_id_nivel_fkey FOREIGN KEY (id_nivel) REFERENCES public.nivel(id_nivel);


--
-- TOC entry 4962 (class 2606 OID 16832)
-- Name: diccionario_base diccionario_base_id_tipo_archivo_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.diccionario_base
    ADD CONSTRAINT diccionario_base_id_tipo_archivo_fkey FOREIGN KEY (id_tipo_archivo) REFERENCES public.tipos_archivo(id_tipo_archivo);


--
-- TOC entry 4963 (class 2606 OID 16852)
-- Name: diccionario_base diccionario_base_id_tipo_palabra_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.diccionario_base
    ADD CONSTRAINT diccionario_base_id_tipo_palabra_fkey FOREIGN KEY (id_tipo_palabra) REFERENCES public.tipo_palabra(id_tipo_palabra);


--
-- TOC entry 4964 (class 2606 OID 16865)
-- Name: diccionario_uso diccionario_uso_id_diccionario_base_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.diccionario_uso
    ADD CONSTRAINT diccionario_uso_id_diccionario_base_fkey FOREIGN KEY (id_diccionario_base) REFERENCES public.diccionario_base(id_diccionario_base);


-- Completed on 2026-05-28 12:37:18

--
-- PostgreSQL database dump complete
--



