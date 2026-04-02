# Swiss Ephemeris Data Files

This directory is where the Swiss Ephemeris `.se1` data files should be placed.
The API will not function without these files — `/health` will return 503.

> **Important**: The file extension is `.se1`, not `.se`.
> The older `.se` format has been deprecated. Use only `.se1` files.

## Required Files

All three files are required for full functionality:


| File          | Covers                              | Download                                                                             |
| ------------- | ----------------------------------- | ------------------------------------------------------------------------------------ |
| `sepl_18.se1` | Sun–Pluto (Jupiter–Pluto, DE431)    | [GitHub](https://raw.githubusercontent.com/aloistr/swisseph/master/ephe/sepl_18.se1) |
| `semo_18.se1` | Moon (lunar ephemeris)              | [GitHub](https://raw.githubusercontent.com/aloistr/swisseph/master/ephe/semo_18.se1) |
| `seas_18.se1` | Fixed star catalog (30 major stars) | [GitHub](https://raw.githubusercontent.com/aloistr/swisseph/master/ephe/seas_18.se1) |


Quick download script:

```bash
curl -o ephe/sepl_18.se1 https://raw.githubusercontent.com/aloistr/swisseph/master/ephe/sepl_18.se1
curl -o ephe/semo_18.se1 https://raw.githubusercontent.com/aloistr/swisseph/master/ephe/semo_18.se1
curl -o ephe/seas_18.se1 https://raw.githubusercontent.com/aloistr/swisseph/master/ephe/seas_18.se1
```

## Extended Time Range (Optional)

The standard files above cover **1301–1701 AD**. For historical or future calculations
outside this range, download the full archive (~2.4 GB, covers **13201 BC–17191 AD**):

```bash
curl -L "https://www.dropbox.com/scl/fo/y3naz62gy6f6qfrhquu7u/h?rlkey=ejltdhb262zglm7eo6yfj2940&dl=1" -o ephe/swe_unix.tar.gz
tar -xzf ephe/swe_unix.tar.gz -C ephe/
```

## Asteroid Files (Optional)

Required only if you query Chiron, Ceres, Pallas, Juno, or Vesta.
Download from the Dropbox archive:

```bash
# See https://www.astro.com/swisseph/swedownload_e.htm for the full Dropbox folder structure.
# Asteroid files are organized in astN subdirectories (N = asteroid_number // 1000).
# After downloading, place files in ast0, ast1, etc. subdirectories under this folder.
```

> **Note**: Asteroid files are only available via Dropbox, not GitHub.
> The Dropbox download URL is:
> `https://www.dropbox.com/scl/fo/y3naz62gy6f6qfrhquu7u/h?rlkey=ejltdhb262zglm7eo6yfj2940&dl=1`

## Licensing

The `.se1` data files are distributed by **Astrodienst AG** under their own license:

> Swiss Ephemeris is free for **non-commercial use**. For commercial use,
> a license must be obtained from Astrodienst AG.
> See: [https://www.astro.com/swisseph/swephinfo_e.htm](https://www.astro.com/swisseph/swephinfo_e.htm)

The API source code itself is released under **AGPL-3.0-or-later**.