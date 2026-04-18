#!/bin/bash

echo "Проверка конфигурации git..."

# Получаем текущие значения
user_name=$(git config --global user.name)
user_email=$(git config --global user.email)

need_name=false
need_email=false

# Проверка user.name
if [ -z "$user_name" ]; then
    echo "⚠️ user.name не задан. Устанавливаю значение по умолчанию: LamdaOmicron"
    git config --global user.name "LamdaOmicron"
    user_name="LamdaOmicron"
    need_name=true
else
    echo "✅ user.name = $user_name"
fi

# Проверка user.email
if [ -z "$user_email" ]; then
    echo "⚠️ user.email не задан. Устанавливаю значение по умолчанию: genaz0983@gmail.com"
    git config --global user.email "genaz0983@gmail.com"
    user_email="genaz0983@gmail.com"
    need_email=true
else
    echo "✅ user.email = $user_email"
fi

echo ""
if [ "$need_name" = true ] || [ "$need_email" = true ]; then
    echo "✓ Настройки git обновлены:"
    echo "   user.name  = $user_name"
    echo "   user.email = $user_email"
else
    echo "✓ Все параметры git уже настроены корректно."
fi

# Опция клонирования репозитория lab_2
echo ""
read -p "Хотите клонировать репозиторий lab_2? (y/n): " clone_choice
if [[ "$clone_choice" =~ ^[Yy]$ ]]; then
    echo ""
    # Запрос URL репозитория
    read -p "Введите URL репозитория lab_2 (например, https://github.com/user/lab_2.git): " repo_url
    if [ -z "$repo_url" ]; then
        echo "❌ URL не указан. Клонирование отменено."
    else
        # Запрос директории для клонирования (по умолчанию текущая)
        read -p "Введите директорию для клонирования (оставьте пустым для текущей): " target_dir
        if [ -z "$target_dir" ]; then
            target_dir="."
        fi

        # Проверка существования git
        if ! command -v git &> /dev/null; then
            echo "❌ Git не установлен. Невозможно выполнить клонирование."
        else
            echo "Клонирование репозитория $repo_url в $target_dir ..."
            if git clone "$repo_url" "$target_dir"; then
                echo "✅ Репозиторий успешно клонирован."
            else
                echo "❌ Ошибка при клонировании репозитория."
            fi
        fi
    fi
fi

echo ""
read -p "Нажмите Enter для выхода..."



8mhz;1psq;q6x8;eac5;dstd;man7;kht1;mhk8;myd7;puxg;28bt;q4jr;5cbi3m;gma7;839wt3;mf05;atwh;z6c1;pjir;a2nd;5r67;y5u2;akq3;wv56;3af1;iaed;idmd;iq1q;z4tj;6t16;x9od;w6v6;i7n1;Naturalized_Foreigner;whoknows;infolock;cleanbill;ehfi8j;plgjmq;TimeRipple;bylb;60f8jv;6oai;wyf7dj;6uue86:3;h7le;yf15;gdvjm8;o7btiw;yc9u;eqth7x;gvsfyn;6o4j;qraweh;Fix_Her;gcit;3npz73;mwlu76;08kd;rqcu;SetOpen;0vds;o4uqlf;2s4gcp;hf46;d9a5;wzsr;ohj3;qe7h;6vjg;dxlp;a67q;lza2;7w44;q34q;b6t7;GlimpOSecr_Aoj;8cwa;neqx0e;e7iw;4bfg;xv6q;moxh;f1ff;4vho;3v6i3m;5iol73;g271x5;5xtbff;x1wn;z7jrpa;20kwdb;inrr;n6hs;dw2w43;b53o85;cfv9;TaSkA_Aoj;ovucry;2zcfhs;6z6r;ju39;dp7ojs;ka6i;d0mx;z235;udrw;u1z6gz;mpkj;stalkr;m1l2a2;0fzgen;kojv7p;xdea11;MagicOP
Все подряд. 
3990;7416;8mhz;1psq;q6x8;eac5;dstd;man7;kht1;mhk8;myd7;puxg;28bt;q4jr;5cbi3m;gma7;839wt3;mf05;atwh;z6c1;pjir;a2nd;5r67;y5u2;akq3;wv56;3af1;iaed;idmd;iq1q;z4tj;6t16;x9od;w6v6;i7n1;Naturalized_Foreigner;whoknows;infolock;cleanbill;ehfi8j;plgjmq;TimeRipple;bylb;60f8jv;6oai;wyf7dj;6uue86:3;h7le;yf15;gdvjm8;o7btiw;yc9u;eqth7x;gvsfyn;6o4j;qraweh;Fix_Her;gcit;3npz73;mwlu76;08kd;rqcu;SetOpen;0vds;o4uqlf;2s4gcp;hf46;d9a5;wzsr;ohj3;qe7h;6vjg;dxlp;a67q;lza2;7w44;q34q;b6t7;GlimpOSecr_Aoj;8cwa;neqx0e;e7iw;4bfg;xv6q;moxh;f1ff;4vho;3v6i3m;5iol73;g271x5;5xtbff;x1wn;z7jrpa;20kwdb;inrr;n6hs;dw2w43;b53o85;cfv9;TaSkA_Aoj;ovucry;2zcfhs;6z6r;ju39;dp7ojs;ka6i;d0mx;u1z6gz;stalkr;m1l2a2;0fzgen;kojv7p;xdea11;mikr;o5m5l5;y7p8;ny2auw;esn1;qmh8;ap5s;e6oc;v349;78ba;b4bu;g5ho;pnbj;odac;icayda;2mg15w;bd9roc;TheGreatEvil;nny5n7;8q5rqs;D1vIn0;alvwj2;a9ym8u;qd3oj5;3jhlqr;o5uryd;4a2g29;0t5i5i;g4tb;411h;feuh;h7ey;tobu;dksr;l1cp;tzgz;eour;7tp5;b7avrr;TheOldestOne;w552;3r2fsn;jjzk;flfb0i;ek2w;j3dn;182x9v;t9glnp;25ctxh;cyal9s;9pid66;ShinzaStar;1ewyxr;kqdu50;33xntz;2hxti5;tmgew5;vc9dby;4099x2;yeo00f;wnmv84;z1t88t;InnTalentPsycho;nv8jde;bbio;4zr0;ghhs;b902;suny;dmji;mfbut8;l84cee;Qboard;m75t3aL;3v16e0;i7cvn1;vk5mep;oa0mcv;pig6x6;7zt9ig;mies;fa9v0q;151dg6;76pb;tuccek;pz3p;4gwhdq;6nul;mntj;htli;vf9x;euu5;n00i;ew9q;rd6x;ocvl;3hlfsj;l4hv;e70bpv;i3il9t;8f7i;sr7w;tkom;37myl4;beq4yk;2gyi;e04o97;3tbvoj;r4zex0;ejar4y;6c2esk;wfv83t;Resistance;FaeHand;1id6y8;6oer4t;uybx3s;kwiyja;e4w8;50guut;makjg9;li0j5x;gpn5iw;8nq00b;rsl00z;2tbf84;stlwsf;CrownAbove;napc0e;fptk71;ll1o95;jkkljx;eijtyl;jd9vgu;seda404;usukx4;uj8sb8;g7qmfq;yevdy9;c6bclo;NdAaC;5c51in;gyv3ti;m6q1hp;pht46r;z2agg4;sjl201;AdminEng;7nr1i6;5xn5lo;Bloodworms;WIndex;reality_scam;EsoAllNatural;qumw2n;absmrt;oyuoxl;24ltzr;8emw9a;cqxshb;OmniViewpoint;IamAWAKE;mv8b;eo6y;fwoo;wlso;h7uu;KeyNascentSoul;9h011r;ctrq39;pa82;kk0m;NANO1;D1g1v1c3;TactDoll;thro;pe335p;wptrn0;7qo1nj;NanoMancer;ryyl96;cdw9;e2ei;gekl;God_SEED;ru679z;p74l;TriPwr;TriCrg;TriWis;6z8u7p;AstralFork;gftguq;Gugalanna;cckmhe;ep5t;InvisAir;laon;y5qht2;s0LoM4NkEy5;s2yl7f;n8er;oaen;2zlke4;BlasphemySlate:2;5jhtfw;lg59lo;dojb0v;m3mkdi;DungeonCoreOoP;qrlidh;qemm;hfm4xg;TreeDiagram;Ruina.Lib;l5wrr4;gyku;g1cxlz;906vb3;ojgujg;ecn2gs;j45mhw;ekmi0c;8c0u9o;c2qcw8;91wcm7;87r6dr;le5wik;WizardBathrobe;oytv2k;4nd7uh;CivilightEterna;e4or;fdlmya;5jrjly;vjbm;dws4;DiadRR;LockSS;0yu8;6ewp;6ewp2;dxqu88;0ghd;One_Ring;MetalVessel;7qk192;AkatsukiRings;v7vu3f;jsiqhz;j91xkc;fk9lk7;megane;oaf2;gqx7ol;4olq;FantasyEyes;d868;xecx;cojp;k775;wj53;x9x4;ppjb;8nw3;8m9p;g5b4;xr34;zh97lc;b2jj;nh14f8;glo00l;xwbv6d;gq6hc4;cwpdji;6yluz1;gaia0n;ct2ua4;to92t1;3a5itf;uda2en;93n4pk;BetterPanPan;G3ENmA83;byh33g;b9148e;R3DmA83;r72lvl;BlackMage;93oaw7;utlblf;5760k0;mh95gi;0f2p3n;iam5ke;tdp7hm;Arsscire;ywiav7;g84uhe;forcemg;1x1dyj;BudgetPotions;1m2byp;mn700w;MagicPowerTai;2m5okd;yna77d;j0nrbw;rune;196cmx;zcrd2q;83ifwu;lyut;afbb;prr79j;ajdi;bzb0;r4yq;91b7d9;pb4w;di9g;hycx;f4fq;64yj;9kx4;k4sv;g4iu;vf1haj;3d25;o3bj;jym5;gpem;70pssv;81ky;hhgq;es3f;b378;x905;s42x;8si9;KokyuHoho;0nku;4amq;Keraunos;n6skh3;gi5hb1;CursedMud;FlowerPowerShield;RichardExalibur;2hrck4;RichardLionheart;jtw7uw;UomoUniversale;l6nj;dy8n;s3hf;o3y1gc;kwhv;dn4mb5;wxd7my;fudzcd;fidqly;fa2rpf;uucx;yrcl;9kt0;m3f3ld;rx88f3;kplqf4;uoa6zg;okexu0;b3xrep;wb57xg;odyu;1tfh;6d4t;BlackofVenus;h31p8u;ogq6;pr09s8;1tyyxq;yqr7;ngjx;24zsss;onjv;j0kj;1mq8;Mag;Madoka;sf8f:7;mqwr;w3ed;l9rc;ry99;a576;4z5b;heuo;ee74vr;bf35k5;n40n;68jw63;a16f4f;xrqkhh;OriginArts;v6gh;rmcljy;IttouShura;Noita;wdaxgw;ToTalkWithAGod;rzymjl;y025mn;bloodsign;holy7th;g60zt2;ap8ahq;MagExp;2lbpi6;biahbm;xn99rp;gb6n;sxy7;nzjwc6;c3anq8;g38lan;Homebody;bclh9c;tgqh6o;18gwdo;atvp8u;FairyFateofWinx;MageCore;ManaConstructs;759c;9dwu;p9ud;uank;33mm;4t6ml0;ldd79r;vqzmjf;MinMas;wra5ip;xpo7rw;md1k0k;evw38n;dipelo;z2qz8r;zyla5d;o8haj3;RecPresence;l9rdew;2sfec4;sgfurc;7q02ec;va5xqq;0eh9;Merlin_Eyes;nyjx;dvvjrz;TrueMEye;DreamfortheStars;rufi2v;HumanObsrv;5aed;c5bsi0;fo3s;9ss6;q4d4;zdj7;3vf6;qzl3;kid5;gsdj;ouajca;zht26a;wl5o;pkins2;mgv4;mmt9ky;9grq48;qbone1;qqdvrw;mom6vj;kglzo7;npez;ppdr;8nvi;wjb3;m85q;z3yz;qlsa90;2xrwxt;pe9e1r;glow96;jvid1c;2yie4n;19olr5;i0f9px;2b7jq2;qegi6g;Merfolk;4i1dn4;ijedt9;mzkcq3;vaaryv;enk4z7;5q5yz7;dejqut;kqjt6l;r0gg3d;6r34dj;RoyalBody;o656qq;DeadApostle;eee3;jyx3;sqfsco;BattleCon;ThreeStage;IaidoGensai;hju5;x00l3c;xv3bpl;jon92;ewb6;hzd5;4vah;m2t5t8;d80qyn;wexv8w;v60g;yme1;is4h3v;9owk;ChiyouRoRagnarok;e1vb;sn0k;yha5;540e;mgnj;zzxd;3e22;f9kj;8ats;exu2;jynm;a7zo;hi4l;c3i92e;emli;cdyd0d;zUdQE;6gnhl1;oouphx;vdu536;2wc4kw;u6tb3p;Ancients;Teekaz;ot4x;r03vac;MANTIS;6e3tdf;mffzvs;xdvgot;17wqnv;hnbaco;6jh9l9;eezpxz;wbg8nk;khbaie;8v6xoj;gks5mg;n4006o;iiw7q4;xvi5cb;klcc2z;8iow6t;o05egs;MindDragon;4gp822;o4bzgx;harfkm;csvp;vkl0;ojin;6xa3;1gay;kpwp;soqi;83ur;hhxn;u6dv;a1ys;hf0glh;4hoy;w10y;cssrc5;1975so;1k4af1;fsaz2e;kkc9k6;1x0dqx;az3pq1;ul77pv;82r384;g2fkml;fg576k;3bhnb7;u6kxsk;0op5fh;w5w4r6;ttt0jl;7oa77q;sxajnn;58gt3h;2ttxwl