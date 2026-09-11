# daksh1136 animated GitHub profile

## Push

```powershell
gh auth login
.\setup-profile.ps1
```

Create `daksh1136/daksh1136` as a **public** GitHub repository first if it does not exist.

## Generate the live graph

After pushing:

**GitHub → Actions → Update profile art → Run workflow**

## Local generation

```powershell
python -m pip install -r scripts/requirements.txt
python scripts/fetch_contributions.py
python scripts/render_heatmap_svg.py
```
