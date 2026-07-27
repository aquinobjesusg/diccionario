import {
  Mic,
  Sparkles,
  Repeat,
  Globe2,
  MessagesSquare,
  Trophy,
} from "lucide-react";

const features = [
  {
    icon: Mic,
    title: "Pronunciación en tiempo real",
    desc: "Habla y recibe correcciones instantáneas con reconocimiento de voz adaptado a tu acento.",
  },
  {
    icon: Sparkles,
    title: "Vocabulario espontáneo",
    desc: "Aprende palabras y frases que realmente se usan en el día a día, no solo en libros.",
  },
  {
    icon: Repeat,
    title: "Repaso inteligente",
    desc: "Recordatorio espaciado que trae cada término de vuelta justo antes de que lo olvides.",
  },
  {
    icon: Globe2,
    title: "Contexto cultural",
    desc: "Descubre modismos, expresiones y matices de diferentes regiones del mundo anglófono.",
  },
  {
    icon: MessagesSquare,
    title: "Conversaciones guiadas",
    desc: "Practica diálogos reales con escenarios cotidianos: viajes, trabajo, social.",
  },
  {
    icon: Trophy,
    title: "Progreso visible",
    desc: "Sube de nivel, desbloquea logros y mantén tu racha de aprendizaje viva.",
  },
];

export function FeatureGrid() {
  return (
    <section className="mx-auto max-w-6xl px-6 py-16 md:py-24">
      <div className="mb-12 text-center">
        <h2 className="font-serif text-3xl font-bold text-sky-950 md:text-4xl">
          Todo lo que necesitas para dominar el inglés
        </h2>
        <p className="mx-auto mt-4 max-w-2xl text-sky-950/80">
          Diccionario, práctica y comunidad en una sola aplicación diseñada
          para que aprendas de forma natural y sin esfuerzo.
        </p>
      </div>

      <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {features.map((f) => (
          <div
            key={f.title}
            className="group rounded-2xl border border-sky-400/70 bg-white/90 p-6 shadow-sm backdrop-blur transition-all hover:-translate-y-1 hover:border-sky-500 hover:bg-white hover:shadow-lg hover:shadow-sky-400/50"
          >
            <div className="mb-4 inline-flex h-12 w-12 items-center justify-center rounded-xl bg-sky-200 text-sky-800 transition-colors group-hover:bg-sky-700 group-hover:text-white">
              <f.icon className="h-6 w-6" strokeWidth={1.8} />
            </div>
            <h3 className="text-lg font-semibold text-sky-950">{f.title}</h3>
            <p className="mt-2 text-sm leading-relaxed text-sky-900/80">
              {f.desc}
            </p>
          </div>
        ))}
      </div>
    </section>
  );
}