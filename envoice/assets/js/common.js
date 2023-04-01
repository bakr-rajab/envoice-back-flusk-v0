function sidebarToggling(){
    const SIDEBAR_EL = document.getElementById("sidebar");
       
       document.getElementById("btn-collapse").addEventListener("click", () => {
         SIDEBAR_EL.classList.toggle("sidebar-collapsed");
       
       });

}

function paggnation(){
    $(document).ready(function() {
        $('#example').DataTable( {
          "bSort": false,
        "language": {
          "lengthMenu": "عرض _MENU_ تسجيلات لكل صفحة",
          "zeroRecords": "لا يوجد نتائج للبحث",
          "info": "عرض صفحة _PAGE_ من _PAGES_",
          "infoEmpty": "لا يوجد تسجيلات متاحة",
          "infoFiltered": "(تم الفلترة من _MAX_ total records)",
          "loadingRecords": "جارٍ التحميل...",
        "lengthMenu": "أظهر _MENU_ مدخلات",
          "zeroRecords": "لم يعثر على أية سجلات",
          "info": "عرض صفحة _PAGE_ من _PAGES_",
          "infoEmpty": "لا يوجد تسجيلات متاحة",
          "infoFiltered": "(منتقاة من مجموع _MAX_ مُدخل)",
          "sSearch":        "بحث عن:",
          "info": "إظهار _START_ إلى _END_ من أصل _TOTAL_ مدخل",
          "search": "ابحث:",
          "paginate": {
          "first": "الأول",
          "previous": "السابق",
          "next": "التالي",
          "last": "الأخير",
          }
        
        }
        } );
        } );
}

function disableOthers(index){
  document.getElementById(index).disabled = true;
}

function enableAll(index){
  document.getElementById(index).disabled = false;
}

// $(document).ready(function () {
//   $('select').selectize({
//       sortField: 'text'
//   });
// });

// $(document).ready(function() {
  
//   $(".js-select2").select2();

  
// });