from pathlib import Path
import shutil
import subprocess


def run(*args, cwd):
    print("+", " ".join(args))
    subprocess.run(args, cwd=cwd, check=True)


def main():
    project = Path(input("Chemin complet du dossier github_ready_vatencul_lidar : ").strip().strip('"')).expanduser().resolve()
    repo_url = input("URL GitHub (https://github.com/UTILISATEUR/DEPOT.git) : ").strip()
    if not project.is_dir():
        raise SystemExit(f"Dossier introuvable : {project}")
    if not shutil.which("git"):
        raise SystemExit("Git n'est pas installé : https://git-scm.com/downloads")
    too_large = [p for p in project.rglob("*") if p.is_file() and p.stat().st_size >= 100 * 1024 * 1024]
    if too_large:
        raise SystemExit("Fichiers >=100 Mio :\n" + "\n".join(map(str, too_large)))
    if not (project / ".git").exists():
        run("git", "init", cwd=project)
    if not subprocess.run(["git", "config", "user.name"], cwd=project, capture_output=True).stdout.strip():
        run("git", "config", "user.name", input("Nom à associer aux commits : ").strip(), cwd=project)
    if not subprocess.run(["git", "config", "user.email"], cwd=project, capture_output=True).stdout.strip():
        run("git", "config", "user.email", input("E-mail à associer aux commits : ").strip(), cwd=project)
    run("git", "branch", "-M", "main", cwd=project)
    run("git", "add", "--all", cwd=project)
    status = subprocess.run(["git", "status", "--porcelain"], cwd=project, text=True, capture_output=True, check=True).stdout
    if status:
        run("git", "commit", "-m", "Publication initiale du mémoire LiDAR Vatencul", cwd=project)
    remotes = subprocess.run(["git", "remote"], cwd=project, text=True, capture_output=True, check=True).stdout.split()
    run("git", "remote", "set-url", "origin", repo_url, cwd=project) if "origin" in remotes else run("git", "remote", "add", "origin", repo_url, cwd=project)
    run("git", "push", "-u", "origin", "main", cwd=project)
    print(f"Import terminé : {repo_url}")


if __name__ == "__main__":
    main()
