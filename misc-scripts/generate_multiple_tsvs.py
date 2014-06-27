__author__ = 'Saksham'

import os

def main():

    dir_path = 'H:\\work_images\\'

    file_name = 'acer_liquid_userdata.dd'
    path = dir_path + file_name
    os.system("yapr_summarize-chunks.py " + path + " -t 30 --name \"Vidas Acer Liquid\"")

    file_name = 'cz_02_huawei_u8510_mtd5_userdata.bin'
    path = dir_path + file_name
    os.system("yapr_summarize-chunks.py " + path + " -t 0 --name \"Simson Huawei U8510-1\"")

    file_name = 'cz_03_htc_pc49100_mtd6_userdata.bin'
    path = dir_path + file_name
    os.system("yapr_summarize-chunks.py " + path + " -t 0 --name \"Simson HTC-PC49100\"")

    file_name = 'htc_desire_userdata.dd'
    path = dir_path + file_name
    os.system("yapr_summarize-chunks.py " + path + " -t 30 --name \"Vidas HTC Desire\"")

    file_name = 'htc-evo-4g-userdata.dd'
    path = dir_path + file_name
    os.system("yapr_summarize-chunks.py " + path + " -t 30 --name \"Vidas HTC-evo-4g\"")

    file_name = 'il_13_huawei_8150_mtd6_userdata.bin'
    path = dir_path + file_name
    os.system("yapr_summarize-chunks.py " + path + " -t 0 --name \"Simson Huawei-8150\"")

    file_name = 'in_p_005_moto_mb502_mtd9_userdata.bin'
    path = dir_path + file_name
    os.system("yapr_summarize-chunks.py " + path + " -t 0 --name \"Simson GSM-MB502-Charm\"")

    file_name = 'in_p_008_htc_wildfire_a333_mtd5_userdata.bin'
    path = dir_path + file_name
    os.system("yapr_summarize-chunks.py " + path + " -t 0 --name \"Simson HTC Wildfire-A333\"")

    file_name = 'in_p_011_dell_xcd35_mtd6_userdata.bin'
    path = dir_path + file_name
    os.system("yapr_summarize-chunks.py " + path + " -t 0 --name \"Simson Dell XCD35\"")

    file_name = 'in_p_014_huawei_u8150_ideos_mtd6_userdata.bin'
    path = dir_path + file_name
    os.system("yapr_summarize-chunks.py " + path + " -t 0 --name \"Simson U8150-Ideos\"")

    file_name = 'in_p_019_dell_xcd28_mtd5_userdata.bin'
    path = dir_path + file_name
    os.system("yapr_summarize-chunks.py " + path + " -t 0 --name \"Simson Dell XCD-28\"")

    file_name = 'in_p_023_htc_nexus_one_mtd5_userdata.bin'
    path = dir_path + file_name
    os.system("yapr_summarize-chunks.py " + path + " -t 0 --name \"Simson HTC Nexus-One\"")

    file_name = 'lg_optimus_userdata.dd'
    path = dir_path + file_name
    os.system("yapr_summarize-chunks.py " + path + " -t 30 --name \"Vidas LG-Optimus\"")

    file_name = 'moto_droid_og_userdata.dd'
    path = dir_path + file_name
    os.system("yapr_summarize-chunks.py " + path + " -t 2 --name \"Vidas Moto-Droid\"")

    file_name = 'uk_07_huawei_barcelona_mtd6_userdata.bin'
    path = dir_path + file_name
    os.system("yapr_summarize-chunks.py " + path + " -t 0 --name \"Simson Huawei-Barcelona\"")

    file_name = 'xperia_mini_pro_userdata.dd'
    path = dir_path + file_name
    os.system("yapr_summarize-chunks.py " + path + " -t 30 --name \"Vidas xperia-mini-pro\"")

    file_name = 'yaffs2-droid-eris-postdeletion.nanddump'
    path = dir_path + file_name
    os.system("yapr_summarize-chunks.py " + path + " -t 30 --name \"Via droid-eris\"")

    file_name = 'yaffs2-htc-aria-postdeletion.nanddump'
    path = dir_path + file_name
    os.system("yapr_summarize-chunks.py " + path + " -t 30 --name \"Via htc-aria\"")

    file_name = 'yaffs2-htc-g1-postdeletion.nanddump'
    path = dir_path + file_name
    os.system("yapr_summarize-chunks.py " + path + " -t 30 --name \"Via htc-G1\"")

    file_name = 'yaffs2-htc-hero-postdeletion.nanddump'
    path = dir_path + file_name
    os.system("yapr_summarize-chunks.py " + path + " -t 30 --name \"Via htc-hero\"")

    file_name = 'yaffs2-htc-mytouch-3g-postdeletion.nanddump'
    path = dir_path + file_name
    os.system("yapr_summarize-chunks.py " + path + " -t 30 --name \"Via htc-mytouch-3g\"")

    file_name = 'yaffs2-lg-optimus-s-postdeletion.nanddump'
    path = dir_path + file_name
    os.system("yapr_summarize-chunks.py " + path + " -t 30 --name \"Via LG-Optimus-S\"")

    file_name = 'yaffs2-motorola-droid-postdeletion.nanddump'
    path = dir_path + file_name
    os.system("yapr_summarize-chunks.py " + path + " -t 2 --name \"Via moto-droid\"")

    file_name = 'yaffs2-nexus-one-postdeletion.nanddump'
    path = dir_path + file_name
    os.system("yapr_summarize-chunks.py " + path + " -t 30 --name \"Via nexus-one\"")

    file_name = 'yaffs2-sony-x10-postdeletion.nanddump'
    path = dir_path + file_name
    os.system("yapr_summarize-chunks.py " + path + " -t 30 --name \"Via sony-x10\"")

if __name__ == '__main__':
    main()