 // Complete Data for 58 Wilayas of Algeria with Real Highway Route Coordinates & Distances
        const WILAYAS = [
            { code: 1,  en: "Adrar",          fr: "Adrar",          ar: "أدرار",            lat: 27.8742, lng: -0.2939, dist: 1400 },
            { code: 2,  en: "Chlef",          fr: "Chlef",          ar: "الشلف",            lat: 36.1652, lng: 1.3345,  dist: 200 },
            { code: 3,  en: "Laghouat",       fr: "Laghouat",       ar: "الأغواط",          lat: 33.8000, lng: 2.8651,  dist: 400 },
            { code: 4,  en: "Oum El Bouaghi", fr: "Oum El Bouaghi", ar: "أم البواقي",       lat: 35.8754, lng: 7.1135,  dist: 500 },
            { code: 5,  en: "Batna",          fr: "Batna",          ar: "باتنة",            lat: 35.5559, lng: 6.1741,  dist: 430 },
            { code: 6,  en: "Béjaïa",         fr: "Béjaïa",         ar: "بجاية",            lat: 36.7558, lng: 5.0843,  dist: 240 },
            { code: 7,  en: "Biskra",         fr: "Biskra",         ar: "بسكرة",            lat: 34.8502, lng: 5.7280,  dist: 400 },
            { code: 8,  en: "Béchar",         fr: "Béchar",         ar: "بشار",             lat: 31.6167, lng: -2.2167, dist: 950 },
            { code: 9,  en: "Blida",          fr: "Blida",          ar: "البليدة",          lat: 36.4700, lng: 2.8300,  dist: 50 },
            { code: 10, en: "Bouira",         fr: "Bouira",         ar: "البويرة",          lat: 36.3749, lng: 3.9020,  dist: 120 },
            { code: 11, en: "Tamanrasset",   fr: "Tamanrasset",   ar: "تمنراست",         lat: 22.7850, lng: 5.5228,  dist: 1900 },
            { code: 12, en: "Tébessa",        fr: "Tébessa",        ar: "تبسة",             lat: 35.4042, lng: 8.1242,  dist: 630 },
            { code: 13, en: "Tlemcen",        fr: "Tlemcen",        ar: "تلمسان",           lat: 34.8783, lng: -1.3150, dist: 520 },
            { code: 14, en: "Tiaret",         fr: "Tiaret",         ar: "تيارت",            lat: 35.3710, lng: 1.3169,  dist: 280 },
            { code: 15, en: "Tizi Ouzou",     fr: "Tizi Ouzou",     ar: "تيزي وزو",         lat: 36.7118, lng: 4.0459,  dist: 100 },
            { code: 16, en: "Alger",          fr: "Alger",          ar: "الجزائر",          lat: 36.7538, lng: 3.0588,  dist: 0 },
            { code: 17, en: "Djelfa",         fr: "Djelfa",         ar: "الجلفة",           lat: 34.6728, lng: 3.2630,  dist: 300 },
            { code: 18, en: "Jijel",          fr: "Jijel",          ar: "جيجل",             lat: 36.8205, lng: 5.7667,  dist: 350 },
            { code: 19, en: "Sétif",          fr: "Sétif",          ar: "سطيف",             lat: 36.1911, lng: 5.4137,  dist: 300 },
            { code: 20, en: "Saïda",          fr: "Saïda",          ar: "سعيدة",            lat: 34.8303, lng: 0.1517,  dist: 430 },
            { code: 21, en: "Skikda",         fr: "Skikda",         ar: "سكيكدة",           lat: 36.8792, lng: 6.9042,  dist: 470 },
            { code: 22, en: "Sidi Bel Abbès", fr: "Sidi Bel Abbès", ar: "سيدي بلعباس",     lat: 35.1899, lng: -0.6308, dist: 440 },
            { code: 23, en: "Annaba",         fr: "Annaba",         ar: "عنابة",            lat: 36.9000, lng: 7.7667,  dist: 540 },
            { code: 24, en: "Guelma",         fr: "Guelma",         ar: "قالمة",            lat: 36.4621, lng: 7.4261,  dist: 500 },
            { code: 25, en: "Constantine",    fr: "Constantine",    ar: "قسنطينة",          lat: 36.3650, lng: 6.6147,  dist: 400 },
            { code: 26, en: "Médéa",          fr: "Médéa",          ar: "المدية",           lat: 36.2642, lng: 2.7539,  dist: 80 },
            { code: 27, en: "Mostaganem",     fr: "Mostaganem",     ar: "مستغانم",          lat: 35.9311, lng: 0.0892,  dist: 350 },
            { code: 28, en: "M'Sila",         fr: "M'Sila",         ar: "المسيلة",          lat: 35.7058, lng: 4.5419,  dist: 240 },
            { code: 29, en: "Mascara",        fr: "Mascara",        ar: "معسكر",            lat: 35.3966, lng: 0.1403,  dist: 380 },
            { code: 30, en: "Ouargla",        fr: "Ouargla",        ar: "ورقلة",            lat: 31.9497, lng: 5.3250,  dist: 800 },
            { code: 31, en: "Oran",           fr: "Oran",           ar: "وهران",            lat: 35.6971, lng: -0.6308, dist: 410 },
            { code: 32, en: "El Bayadh",      fr: "El Bayadh",      ar: "البيض",            lat: 33.6831, lng: 1.0192,  dist: 520 },
            { code: 33, en: "Illizi",         fr: "Illizi",         ar: "إليزي",            lat: 26.4833, lng: 8.4667,  dist: 1750 },
            { code: 34, en: "Bordj Bou Arreridj", fr: "Bordj Bou Arreridj", ar: "برج بوعريريج", lat: 36.0732, lng: 4.7611, dist: 240 },
            { code: 35, en: "Boumerdès",      fr: "Boumerdès",      ar: "بومرداس",          lat: 36.7664, lng: 3.4772,  dist: 45 },
            { code: 36, en: "El Tarf",        fr: "El Tarf",        ar: "الطارف",           lat: 36.7672, lng: 8.3138,  dist: 600 },
            { code: 37, en: "Tindouf",        fr: "Tindouf",        ar: "تندوف",            lat: 27.6711, lng: -8.1478, dist: 1750 },
            { code: 38, en: "Tissemsilt",     fr: "Tissemsilt",     ar: "تسمسيلت",          lat: 35.6072, lng: 1.8106,  dist: 220 },
            { code: 39, en: "El Oued",        fr: "El Oued",        ar: "الوادي",           lat: 33.3683, lng: 6.8674,  dist: 620 },
            { code: 40, en: "Khenchela",      fr: "Khenchela",      ar: "خنشلة",            lat: 35.4358, lng: 7.1433,  dist: 500 },
            { code: 41, en: "Souk Ahras",     fr: "Souk Ahras",     ar: "سوق أهراس",        lat: 36.2864, lng: 7.9511,  dist: 640 },
            { code: 42, en: "Tipaza",         fr: "Tipaza",         ar: "تيبازة",           lat: 36.5897, lng: 2.4475,  dist: 70 },
            { code: 43, en: "Mila",           fr: "Mila",           ar: "ميلة",             lat: 36.4503, lng: 6.2644,  dist: 380 },
            { code: 44, en: "Aïn Defla",      fr: "Aïn Defla",      ar: "عين الدفلى",       lat: 36.2641, lng: 1.9679,  dist: 140 },
            { code: 45, en: "Naâma",          fr: "Naâma",          ar: "النعامة",          lat: 33.2667, lng: -0.3167, dist: 650 },
            { code: 46, en: "Aïn Témouchent", fr: "Aïn Témouchent", ar: "عين تموشنت",       lat: 35.2975, lng: -1.1404, dist: 450 },
            { code: 47, en: "Ghardaïa",       fr: "Ghardaïa",       ar: "غرداية",           lat: 32.4900, lng: 3.6733,  dist: 600 },
            { code: 48, en: "Relizane",       fr: "Relizane",       ar: "غليزان",           lat: 35.7372, lng: 0.5558,  dist: 300 },
            { code: 49, en: "Timimoun",       fr: "Timimoun",       ar: "تيميمون",          lat: 29.2639, lng: 0.2310,  dist: 1200 },
            { code: 50, en: "Bordj Badji Mokhtar", fr: "Bordj Badji Mokhtar", ar: "برج باجي مختار", lat: 21.3278, lng: 0.9239, dist: 2100 },
            { code: 51, en: "Ouled Djellal",  fr: "Ouled Djellal",  ar: "أولاد جلال",       lat: 34.4278, lng: 5.0681,  dist: 400 },
            { code: 52, en: "Béni Abbès",     fr: "Béni Abbès",     ar: "بني عباس",         lat: 30.1333, lng: -2.1667, dist: 1200 },
            { code: 53, en: "In Salah",       fr: "In Salah",       ar: "عين صالح",         lat: 27.1936, lng: 2.4607,  dist: 1300 },
            { code: 54, en: "In Guezzam",     fr: "In Guezzam",     ar: "عين قزام",         lat: 19.5686, lng: 5.7692,  dist: 2300 },
            { code: 55, en: "Touggourt",      fr: "Touggourt",      ar: "تقرت",             lat: 33.1053, lng: 6.0583,  dist: 620 },
            { code: 56, en: "Djanet",         fr: "Djanet",         ar: "جانت",             lat: 24.5533, lng: 9.4836,  dist: 2100 },
            { code: 57, en: "El M'Ghair",     fr: "El M'Ghair",     ar: "المغير",           lat: 33.9500, lng: 5.9167,  dist: 550 },
            { code: 58, en: "El Meniaa",      fr: "El Meniaa",      ar: "المنيعة",          lat: 30.5833, lng: 2.8833,  dist: 870 },
            { code: 59, en: "Aflou",          fr: "Aflou",       ar: "آفلو",           lat: 34.1128, lng: 2.1023,  dist: 306  },
            { code: 60, en: "Barika",         fr: "Barika",       ar: " بريكة",           lat: 35.38901, lng: 5.36584,  dist: 258 },
            { code: 61, en: "El Kantara",     fr: "El Kantara",       ar: " القنطرة",           lat: 35.2225, lng: 5.7067,  dist: 293 },
            { code: 62, en: "Bir El Ater",    fr: "Bir El Ater",       ar: "بئر العاتر",          lat: 34.74488, lng: 8.06024,  dist: 504 },
            { code: 63, en: "El Aricha",      fr: "El Aricha", ar: "العريشة", lat: 34.2227, lng: -1.2557, dist: 578 },
            { code: 64, en: "Ksar Chellala",  fr: "Ksar Chellala",  ar: "قصر الشلالة",       lat: 35.2122, lng: 2.3189,  dist: 138 },
            { code: 65, en: "Aïn Oussara",    fr: "Aïn Oussara",     ar: "عين وسارة",         lat: 35.45139, lng: 2.90583, dist: 145 },
            { code: 66, en: "Messaad",        fr: "Messaad",       ar: "مسعد",         lat: 34.1543, lng: 3.5031,  dist: 371 },
            { code: 67, en: "Ksar El Boukhari",fr: "Ksar El Boukhari",     ar: "قصر البخاري",         lat: 35.88889, lng: 2.74905,  dist: 141 },
            { code: 68, en: "Bou Saâda",       fr: "Bou Saâda",      ar: " بوسعادة",             lat: 35.21324, lng: 4.18048,  dist: 240 },
            { code: 69, en: "El Abiodh Sidi Cheikh", fr: "El Abiodh Sidi Cheikh",         ar: "الأبيض سيدي الشيخ",             lat: 32.89648, lng: 0.54639,  dist: 610 },
            { code: 69, en: "Ain Amenas", fr: "Ain Amenas",         ar: "إن أميناس",             lat:  28.03867, lng: 9.57615,  dist: 1508 },
            { code: 69, en: "Hassi Messaoud", fr: "Hassi Messaoud",         ar: " حاسي مسعود",             lat: 31.6804, lng: 6.0729,  dist: 856}
        ];

        // Language Dictionary
        const TRANSLATIONS = {
            en: {
                subtitle: "Algeria Highway & Travel Cost Estimator",
                title: "Journey Parameters",
                desc: "Origin set to Algiers (16). Choose destination and vehicle specs.",
                lblDepart: "Departure Wilaya",
                lblDest: "Destination Wilaya",
                lblVehicle: "Vehicle Category",
                lblFuel: "Handling",
                lblhzrd:"Hazardous Product",
                lblwght:"Weight",
                lblConsumption: "Avg. Consumption",
                lblFuelPrice: "Fuel Unit Price",
                lblPassengers: "Passengers",
                lblRoundtrip: "Round Trip (Aller-Retour)",
                lblTolls: "Include Highway Toll Est.",
                routeMap: "Interactive Route Map",
                totalCost: "Estimated Total Trip Cost",
                perPerson: "Base rate",
                metricDist: "Distance",
                metricTime: "Duration",
                metricFuel: "Fuel Volume",
                breakdownFuel: "Vehicle coefficient",
                breakdownToll: "Difficulty coefficient",
                breakdownWear: "Wear & Maintenance",
                footer: "DzTravel Pro • Travel & Highway Cost Calculator • All 58 Algerian Wilayas"
            },
            fr: {
                subtitle: "Calculateur de Frais de Voyage et Autoroute",
                title: "Paramètres du Trajet",
                desc: "Départ fixé à Alger (16). Choisissez votre destination.",
                lblDepart: "Wilaya de Départ",
                lblDest: "Wilaya de Destination",
                lblVehicle: "Catégorie du Véhicule",
                lblFuel: "Manutention",
                lblhzrd:"Produit Dangereux",
                lblwght:"Poid",
                lblConsumption: "Consommation Moy.",
                lblFuelPrice: "Prix du Carburant",
                lblPassengers: "Passagers",
                lblRoundtrip: "Aller-Retour",
                lblTolls: "Inclure Estimation Péage",
                routeMap: "Carte Interactive du Trajet",
                totalCost: "Coût Total Estimé du Trajet",
                perPerson: "Tarif de base",
                metricDist: "Distance",
                metricTime: "Durée Est.",
                metricFuel: "Volume Carburant",
                breakdownFuel: "Coefficient véhicule",
                breakdownToll: "Coefficient difficulté",
                breakdownWear: "Usure & Entretien",
                footer: "DzTravel Pro • Calculateur de Coût de Voyage • 58 Wilayas d'Algérie"
            },
            ar: {
                subtitle: "حاسبة تكاليف السفر والطريق السريع في الجزائر",
                title: "معطيات الرحلة",
                desc: "نقطة انطلاق مثبتة: الجزائر العاصمة (16). اختر وجهتك.",
                lblDepart: "ولاية الانطلاق",
                lblDest: "ولاية الوصول",
                lblVehicle: "فئة المركبة",
                lblFuel: "مناولة",
                lblhzrd:"منتج خطير",
                lblwght:"وزن",
                lblConsumption: "معدل الاستهلاك",
                lblFuelPrice: "سعر اللتر الواحدة",
                lblPassengers: "عدد الركاب",
                lblRoundtrip: "ذهاب وإياب (Aller-Retour)",
                lblTolls: "إدراج رسوم الطريق السريع",
                routeMap: "خريطة المسار التفاعلية",
                totalCost: "التكلفة الإجمالية التقديرية",
                perPerson: "السعر الأساسي",
                metricDist: "المسافة",
                metricTime: "الزمن المتوقع",
                metricFuel: "حجم الوقود",
                breakdownFuel: "معامل المركبة",
                breakdownToll: "معامل الصعوبة",
                breakdownWear: "الصيانة والاهتلاك",
                footer: "DzTravel Pro • حاسبة تكاليف السفر لجميع الولايات الـ 58"
            }
        };

        // Global App State
        let currentLang = 'en';
        let selectedWilaya = WILAYAS.find(w => w.code === 31); // Default Oran
        let passengerCount = 1;
        let map, routePolyline, algiersMarker, destMarker;
        let costChart;

        // Initialize Map & Dynamic Features on Load
        window.onload = function() {
            initMap();
            initChart();
            populateWilayaDropdown();
            recalculate();
            
            // Close Wilaya dropdown on outside click
            document.addEventListener('click', function(e) {
                const search = document.getElementById('dest-search');
                const dropdown = document.getElementById('wilaya-dropdown');
                if (!search.contains(e.target) && !dropdown.contains(e.target)) {
                    dropdown.classList.add('hidden');
                }
            });
        };

        // Initialize Leaflet Map with Google-Style Dark Tile layer
        function initMap() {
            const algiers = WILAYAS.find(w => w.code === 16);
            
            map = L.map('map', {
                center: [36.25, 1.5],
                zoom: 6,
                zoomControl: true
            });

            // Dark/Modern OpenStreetMap CartoDB Tiles
            L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
                maxZoom: 18,
                subdomains: 'abcd',
                attribution: '&copy; OpenStreetMap &copy; CARTO'
            }).addTo(map);

            // Algiers Marker (Origin)
            const redIcon = L.divIcon({
                className: 'custom-div-icon',
                html: `<div style="background-color: #D21034; width: 16px; h: 16px; border-radius: 50%; border: 3px solid #ffffff; box-shadow: 0 0 10px rgba(210,16,52,0.8);"></div>`,
                iconSize: [16, 16],
                iconAnchor: [8, 8]
            });

            algiersMarker = L.marker([algiers.lat, algiers.lng], { icon: redIcon }).addTo(map)
                .bindPopup("<b>16 - Alger (Origin)</b>");

            // Destination Marker Container
            const goldIcon = L.divIcon({
                className: 'custom-div-icon',
                html: `<div style="background-color: #059669; width: 18px; height: 18px; border-radius: 50%; border: 3px solid #ffffff; box-shadow: 0 0 12px rgba(5,150,105,0.9);"></div>`,
                iconSize: [18, 18],
                iconAnchor: [9, 9]
            });

            destMarker = L.marker([selectedWilaya.lat, selectedWilaya.lng], { icon: goldIcon }).addTo(map);

            // Initial Route
            drawRoute();
        }

        function drawRoute() {
            const algiers = WILAYAS.find(w => w.code === 16);
            
            if (routePolyline) {
                map.removeLayer(routePolyline);
            }

            // Move marker
            destMarker.setLatLng([selectedWilaya.lat, selectedWilaya.lng]);
            destMarker.bindPopup(`<b>${selectedWilaya.code} - ${selectedWilaya.en}</b>`).openPopup();

            // Direct curved/geodesic path visual
            const latlngs = [
                [algiers.lat, algiers.lng],
                [selectedWilaya.lat, selectedWilaya.lng]
            ];

            routePolyline = L.polyline(latlngs, {
                color: '#059669',
                weight: 4,
                opacity: 0.8,
                dashArray: '8, 8',
                lineCap: 'round'
            }).addTo(map);

            // Fit map bounds smoothly
            const bounds = L.latLngBounds(latlngs);
            map.fitBounds(bounds, { padding: [50, 50] });

            // Update Badge Text
            document.getElementById('route-badge').textContent = `Alger → ${selectedWilaya.en}`;
        }

        // Initialize Donut Chart for Breakdown
        function initChart() {
            const ctx = document.getElementById('costChart').getContext('2d');
            costChart = new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: ['Fuel', 'Tolls', 'Maintenance'],
                    datasets: [{
                        data: [70, 15, 15],
                        backgroundColor: ['#059669', '#3b82f6', '#f59e0b'],
                        borderWidth: 0,
                        hoverOffset: 4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false }
                    },
                    cutout: '70%'
                }
            });
        }

        // Populate Custom Wilaya Search Dropdown
        function populateWilayaDropdown() {
            const dropdown = document.getElementById('wilaya-dropdown');
            dropdown.innerHTML = '';

            WILAYAS.forEach(w => {
                if (w.code === 16) return; // Skip Algiers
                
                const item = document.createElement('div');
                item.className = "px-4 py-2.5 hover:bg-emerald-500/10 cursor-pointer flex items-center justify-between text-xs transition-all";
                
                let name = w.en;
                if (currentLang === 'fr') name = w.fr;
                if (currentLang === 'ar') name = w.ar;

                item.innerHTML = `
                    <span class="font-bold text-gray-900 dark:text-gray-100">${w.code} - ${name}</span>
                    <span class="text-[10px] text-gray-400 font-semibold">${w.dist} km</span>
                `;

                item.onclick = function() {
                    selectedWilaya = w;
                    document.getElementById('dest-search').value = `${w.code} - ${name}`;
                    dropdown.classList.add('hidden');
                    recalculate();
                };

                dropdown.appendChild(item);
            });

            // Set initial search input value
            let name = selectedWilaya.en;
            if (currentLang === 'fr') name = selectedWilaya.fr;
            if (currentLang === 'ar') name = selectedWilaya.ar;
            document.getElementById('dest-search').value = `${selectedWilaya.code} - ${name}`;
        }

        function showWilayaDropdown() {
            document.getElementById('wilaya-dropdown').classList.remove('hidden');
        }

        function filterWilayas() {
            const query = document.getElementById('dest-search').value.toLowerCase();
            const dropdown = document.getElementById('wilaya-dropdown');
            dropdown.classList.remove('hidden');

            const children = dropdown.children;
            for (let i = 0; i < children.length; i++) {
                const text = children[i].textContent.toLowerCase();
                if (text.includes(query)) {
                    children[i].style.display = "flex";
                } else {
                    children[i].style.display = "none";
                }
            }
        }

        function onVehicleChange() {
            const select = document.getElementById('vehicle-type');
            const consumption = select.options[select.selectedIndex].getAttribute('data-consumption');
            document.getElementById('consumption-range').value = consumption;
            updateConsumption(consumption);
        }

        function onFuelChange() {
            //const select = document.getElementById('fuel-type');
            //const price = select.options[select.selectedIndex].getAttribute('data-price');
            //document.getElementById('fuel-price-range').value = price;
            //updateFuelPrice(price);
            document.getElementById("fuel-type").value
            recalculate()
        }

        function onHZDChange() {

            isHzrd =document.getElementById("consumption-range").value;
            //
            if (isHzrd ==="oui"){
                //
                console.log(' Hazard Product its yes')
                document.getElementById("lbl-wght-val").disabled = false
                document.getElementById("lbl-wght-lock").innerHTML="<i></i>"
                document.getElementById("lbl-wght-val").classList.remove("cursor-not-allowed")

                //
            }else {
                //
                console.log(' Hazard Product its no')
                document.getElementById("lbl-wght-lock").innerHTML=`<i class="fa-solid fa-lock text-xs"></i>`
                document.getElementById("lbl-wght-val").classList.add("cursor-not-allowed")
                document.getElementById("lbl-wght-val").value = 0
                //
            }

        }

        function onWeigthChange(){

            poid = document.getElementById("lbl-wght-val").value
            console.log('poid ==> ',poid)
            recalculate()
        }

        function updateConsumption(val) {
            //document.getElementById('consumption-val').textContent = `${parseFloat(val).toFixed(1)} L/100km`;
            recalculate();
        }

        function updateFuelPrice(val) {
            document.getElementById('fuel-price-val').textContent = `${parseFloat(val).toFixed(2)} DZD/L`;
            recalculate();
        }

        function adjustPassengers(delta) {
            passengerCount = Math.max(1, Math.min(8, passengerCount + delta));
            document.getElementById('passenger-count').textContent = passengerCount;
            recalculate();
        }

        // Main Calculation Method
        /*function recalculate() {
            if (!selectedWilaya) return;

            //const isRoundTrip = document.getElementById('chk-roundtrip').checked;
            //const includeTolls = document.getElementById('chk-tolls').checked;
            const consumptionL = parseFloat(document.getElementById('consumption-range').value);
            const fuelPrice = parseFloat(document.getElementById('fuel-price-range').value);

            // Distance
            let totalDistance = selectedWilaya.dist;
            //if (isRoundTrip) totalDistance *= 2;

            // Travel Time Estimation (Avg highway speed 80-90 km/h)
            const totalHoursDec = totalDistance / 85;
            const hours = Math.floor(totalHoursDec);
            const mins = Math.round((totalHoursDec - hours) * 60);

            // Fuel Needed
            const totalFuelLiters = (totalDistance / 100) * consumptionL;
            const fuelCost = Math.round(totalFuelLiters * fuelPrice);

            // Estimated Tolls (Autoroute Est-Ouest ~0.8 DZD / km)
            //const tollCost = (includeTolls && totalDistance > 50) ? Math.round(totalDistance * 0.7) : 0;
            tollCost = (totalDistance > 50) ? Math.round(totalDistance * 0.7) : 0;

            // Estimated Vehicle Wear & Maintenance (0.5 DZD / km)
            const wearCost = Math.round(totalDistance * 0.5);

            // Total Cost
            const totalTripCost = fuelCost + tollCost + wearCost;
            const perPersonCost = Math.round(totalTripCost / passengerCount);

            // Update UI Elements
            document.getElementById('total-cost').textContent = totalTripCost.toLocaleString();
            document.getElementById('cost-per-person').textContent = `${perPersonCost.toLocaleString()} DZD`;
            document.getElementById('metric-dist').textContent = `${totalDistance} km`;
            document.getElementById('metric-time').textContent = `${hours}h ${mins}m`;
            document.getElementById('metric-fuel').textContent = `${totalFuelLiters.toFixed(1)} L`;

            document.getElementById('val-fuel-cost').textContent = `${fuelCost.toLocaleString()} DZD`;
            document.getElementById('val-toll-cost').textContent = `${tollCost.toLocaleString()} DZD`;
            document.getElementById('val-wear-cost').textContent = `${wearCost.toLocaleString()} DZD`;

            // Update Chart
            if (costChart) {
                costChart.data.datasets[0].data = [fuelCost, tollCost, wearCost];
                costChart.update();
            }

            // Draw Route on Map
            drawRoute();
        }*/
        //
        function recalculate(){
            // Distance
            let totalDistance = selectedWilaya.dist;
            let vehicle = document.getElementById('vehicle-type').value;
            let consumption =document.getElementById('consumption-range').value;
            let total_consumption = (0.35*Number(selectedWilaya.dist)).toFixed(2)
            let hour = (Number(selectedWilaya.dist)/100).toFixed(0)
            let mins = (Number(selectedWilaya.dist)%100)*0.6
            let manutention =document.getElementById("fuel-type").value
            let poid =document.getElementById("fuel-type").value
            let dangereux= document.getElementById("lbl-wght-val").value
            // Total Cost
            //const totalTripCost = fuelCost + tollCost + wearCost;
            //const perPersonCost = Math.round(totalTripCost / passengerCount);
            //
            console.log("wilaya selected is :",selectedWilaya )
            console.log("Vehicle selected is :",vehicle )
            // Get request for integration my sol
            fetch(`../recalculate?destination=${selectedWilaya.fr}&distance=${selectedWilaya.dist}&vehicule=${vehicle}&manutention=${manutention}&dangereux=${dangereux}&piod=${poid}`)
                .then(response=>response.json())
                .then(json=>{
                    //
                    console.log('data ==> ',json)
                    if(json.code === 200){
                        //
                        // Update UI Elements
                        document.getElementById('total-cost').textContent = Number(json.tarif_total).toFixed(2);
                        document.getElementById('cost-per-person').textContent = Number(json.tarif_base).toFixed(2) + " DZ";
                        document.getElementById('metric-fuel').textContent = total_consumption + " L";
                        //document.getElementById('metric-dist').textContent = Number(selectedWilaya.dist) + " km";
                        document.getElementById('metric-dist').textContent = `${json.distance} km`;
                        //document.getElementById('cost-per-person').textContent = `${perPersonCost.toLocaleString()} DZD`;
                        //document.getElementById('metric-dist').textContent = `${totalDistance} km`;
                        //document.getElementById('metric-time').textContent = `${hour}h ${mins}m`;
                        document.getElementById('metric-time').textContent = `${json.dure}`
                        //document.getElementById('metric-fuel').textContent = `${totalFuelLiters.toFixed(1)} L`;
                        // Update Chart
                        document.getElementById('val-fuel-cost').textContent = 'x' + json.coeff_v;
                        document.getElementById('val-toll-cost').textContent = 'x' + json.coeff_i;
                        // Update Chart
                        if (costChart) {
                            costChart.data.datasets[0].data = [json.coeff_v, json.coeff_i];
                            costChart.update();
                        }
                        //
                    }
                    else{
                        window.alert(`this wilaya ${json.wilaya} not exist`)
                    }
                })
            // Draw Route on Map
            drawRoute();
        }

        // Language Switching Logic
        function setLanguage(lang) {
            currentLang = lang;
            const html = document.documentElement;

            if (lang === 'ar') {
                html.setAttribute('dir', 'rtl');
                html.setAttribute('lang', 'ar');
            } else {
                html.setAttribute('dir', 'ltr');
                html.setAttribute('lang', lang);
            }

            // Update Active Lang Buttons
            ['ar', 'fr', 'en'].forEach(l => {
                const btn = document.getElementById(`btn-lang-${l}`);
                if (l === lang) {
                    btn.className = "px-3 py-1.5 text-xs font-semibold rounded-lg transition-all bg-algeria-green text-white shadow-md";
                } else {
                    btn.className = "px-3 py-1.5 text-xs font-semibold rounded-lg transition-all text-gray-600 dark:text-gray-400 hover:text-emerald-500";
                }
            });

            // Apply Translations
            const t = TRANSLATIONS[lang];
            document.getElementById('header-subtitle').textContent = t.subtitle;
            document.getElementById('form-title').innerHTML = `<i class="fa-solid fa-sliders text-emerald-500"></i> ${t.title}`;
            document.getElementById('form-desc').textContent = t.desc;
            document.getElementById('lbl-depart').innerHTML = `<i class="fa-solid fa-circle-dot text-algeria-red me-1"></i> ${t.lblDepart}`;
            document.getElementById('lbl-dest').innerHTML = `<i class="fa-solid fa-location-dot text-emerald-500 me-1"></i> ${t.lblDest}`;
            document.getElementById('lbl-vehicle').innerHTML = `<i class="fa-solid fa-car text-blue-500 me-1"></i> ${t.lblVehicle}`;
            document.getElementById('lbl-fuel').innerHTML = `<i class="fa-solid fa-gas-pump text-amber-500 me-1"></i> ${t.lblFuel}`;
            document.getElementById('lbl-hzrd').innerHTML = `<i class="fa-solid fa-gas-pump text-amber-500 me-1"></i> ${t.lblhzrd}`;
            document.getElementById('lbl-wght').innerHTML = `<i class="fa-solid fa-circle-dot text-algeria-red me-1"></i> ${t.lblwght}`;
            document.getElementById('lbl-consumption').textContent = t.lblConsumption;
            document.getElementById('lbl-fuel-price').textContent = t.lblFuelPrice;
            //document.getElementById('lbl-passengers').textContent = t.lblPassengers;
            //document.getElementById('lbl-roundtrip').textContent = t.lblRoundtrip;
            //document.getElementById('lbl-tolls').textContent = t.lblTolls;
            document.getElementById('lbl-route-map').textContent = t.routeMap;
            document.getElementById('lbl-total-cost').textContent = t.totalCost;
            document.getElementById('lbl-per-person').textContent = t.perPerson;
            document.getElementById('lbl-metric-dist').textContent = t.metricDist;
            document.getElementById('lbl-metric-time').textContent = t.metricTime;
            document.getElementById('lbl-metric-fuel').textContent = t.metricFuel;
            document.getElementById('lbl-breakdown-fuel').textContent = t.breakdownFuel;
            document.getElementById('lbl-breakdown-toll').textContent = t.breakdownToll;
            //document.getElementById('lbl-breakdown-wear').textContent = t.breakdownWear;
            document.getElementById('footer-text').textContent = t.footer;

            populateWilayaDropdown();
            recalculate();
        }

        // Theme Toggle
        function toggleTheme() {
            const html = document.documentElement;
            if (html.classList.contains('dark')) {
                html.classList.remove('dark');
                html.classList.add('light');
            } else {
                html.classList.remove('light');
                html.classList.add('dark');
            }
        }