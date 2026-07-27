import { BookA, Heart } from "lucide-react";

export function Footer() {
  return (
    <footer className="border-t border-sky-400/60 bg-sky-300/60">
      <div className="mx-auto max-w-6xl px-6 py-12">
        <div className="flex flex-col items-center justify-between gap-6 md:flex-row">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-sky-600 to-emerald-700 shadow-md">
              <BookA className="h-5 w-5 text-white" strokeWidth={1.8} />
            </div>
            <div>
              <p className="font-serif text-lg font-bold text-sky-950">
                DicccSystemsYa
              </p>
              <p className="text-xs text-sky-950/80">
                Aprende inglés, espontáneamente.
              </p>
            </div>
          </div>

          <nav className="flex flex-wrap items-center justify-center gap-x-6 gap-y-2 text-sm text-sky-950/80">
            <a className="transition-colors hover:text-sky-800" href="#">
              Documentación
            </a>
            <a className="transition-colors hover:text-sky-800" href="#">
              Comunidad
            </a>
            <a className="transition-colors hover:text-sky-800" href="#">
              Soporte
            </a>
            <a className="transition-colors hover:text-sky-800" href="#">
              Privacidad
            </a>
          </nav>
        </div>

        <div className="mt-8 flex items-center justify-center gap-1.5 text-xs text-sky-950/70">
          <span>Hecho con</span>
          <Heart className="h-3.5 w-3.5 fill-sky-800 text-sky-800" />
          <span>para quienes aman aprender · © 2025 DicccSystemsYa</span>
        </div>
      </div>
    </footer>
  );
}