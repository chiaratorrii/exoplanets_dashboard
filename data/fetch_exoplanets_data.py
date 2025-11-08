from utils.data_loader import fetch_exoplanet_tap

sql = "select pl_name,hostname,sy_snum,sy_pnum,sy_mnum,discoverymethod,disc_year,disc_facility,disc_instrument,pl_orbper,pl_rade,pl_radj,pl_masse,pl_massj,pl_dens,st_rad,st_mass,sy_dist from ps"
exoplanets = fetch_exoplanet_tap(sql, save_path="exoplanets_data.csv")