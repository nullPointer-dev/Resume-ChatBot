import { useEffect, useState } from "react";
import { SunIcon, MoonIcon } from "@heroicons/react/24/solid";

export default function ThemeToggle() {
  const [theme, setTheme] = useState(
    localStorage.getItem("theme") || 
    (window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light")
  );

  useEffect(() => {
    if (theme === "dark") {
      document.documentElement.classList.add("dark");
      localStorage.setItem("theme", "dark");
    } else {
      document.documentElement.classList.remove("dark");
      localStorage.setItem("theme", "light");
    }
  }, [theme]);

  return (
    <button
      onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
      className="
        p-3 rounded-xl 
        bg-white/10 dark:bg-black/20
        hover:bg-white/20 dark:hover:bg-black/30
        border border-white/20 
        transition-all duration-300
      "
    >
      {theme === "dark" ? (
        <SunIcon className="w-6 h-6 text-yellow-300" />
      ) : (
        <MoonIcon className="w-6 h-6 text-purple-400" />
      )}
    </button>
  );
}
