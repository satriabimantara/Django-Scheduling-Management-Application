$(document).ready(function(){
	/*INPUT DATA PAGE*/
	function inputDataTable(object){
		for (const keys in object) {
			$(object[keys].id).DataTable({
				scrollX: 300,
				scrollY: 450,
				"processing": true,
				buttons: [
				{
					extend :'pdfHtml5',
					className : 'btn-success',
					orientation :'portrait',
					text: '<i class="fas fa-file-pdf" aria-hidden="true"></i> PDF',
					title: object[keys].title,
					extension: ".pdf",
					filename: object[keys].filename,
					pageSize : 'A4'
				},
				{
					extend: 'print',
					className : 'btn-info',
					text: '<i class="fas fa-print"></i> Print',
					title:object[keys].title,
					exportOptions: {
						columns: ':visible',
					}
				},

				],
				"dom": `
				<'row mb-3' <'col-lg-6 d-flex justify-content-start' f> <'col-lg-6 d-flex justify-content-end' l>>+
                <'d-flex justify-content-end' B>+
				<'mb-3' t> +
				<'d-flex justify-content-between mb-5 mt-1'ip>
				`
			});
		}
	}
	const days = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu']
	const tables= {
		table_mata_pelajaran : {
			id : "#tableMataPelajaran",
			title : "Daftar Mata Pelajaran",
			filename : "Daftar Mata Pelajaran"
		},
		table_detail_mata_pelajaran : {
			id : "#tableDetailMataPelajaran",
			title : "Daftar Mapping Mata Pelajaran",
			filename : "Daftar Mapping Mata Pelajaran"
		},
		table_guru : {
			id : "#tableGuru",
			title : "Daftar Guru",
			filename : "Daftar Guru"
		},
		table_detail_kelas : {
			id : "#tableDetailKelas",
			title : "Daftar Kelas Peserta",
			filename : "Daftar Kelas Peserta"
		},
		table_waktu : {
			id : "#tableWaktu",
			title : "Daftar Jam Mata Pelajaran",
			filename : "Daftar Jam Mata Pelajaran"
		},
		table_detail_waktu : {
			id : "#tableDetailWaktu",
			title : "Daftar Detail Waktu Pelajaran",
			filename : "Daftar Detail Waktu Pelajaran"
		},
		table_ruangan : {
			id : "#tableRuangan",
			title : "Daftar Ruangan",
			filename : "Daftar Ruangan"
		},
	};

	// append tabel jadwal setiap hari ke dalam dictionary
	for (const element of days) {
		tables['table_jadwal_'.concat(element)] = {
			id : "#tableJadwal".concat(element),
			title : "Daftar Jadwal Hari ".concat(element),
			filename : "Daftar Jadwal Hari ".concat(element)
		}
		tables['table_revisi_jadwal_'.concat(element)] = {
			id : "#tableRevisiJadwal".concat(element),
			title : "Daftar Revisi Jadwal Hari ".concat(element),
			filename : "Daftar Revisi Jadwal Hari ".concat(element)
		}
	}
	inputDataTable(tables);
});