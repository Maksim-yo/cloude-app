 var current_selected_item;
    $(document).ready(function () {

      $('.upload-btn .upload-btn-input').change(function (ev) {
        console.log('BYTTIN CLI')
        $('.upload-btn .upload-btn-form').submit()
      });
      $('.dropdown-menu #rename_button').on('click', function (ev){
        console.log('TEST')
        var item_id = $(current_selected_item).attr('id');
        $('#form_name_update').attr('action', item_id)

      })
      $('.elm ').click(function (ev) {
      console.log('hello')
        item = this
        if (current_selected_item == item)
          return
        if (current_selected_item)
          $(current_selected_item).attr('style', function (i, s) {
            _str = s || ''
            _str = _str.replace("border-color: #7FCBD8 !important;background: rgba(144, 144, 144, 0.3);", "")
            return _str
          })
        current_selected_item = item
        $(current_selected_item).attr('style', function (i, s) { return (s || '') + 'border-color: #7FCBD8 !important;background: rgba(144, 144, 144, 0.3);' })
      });

      $('.elm ').dblclick(function (ev) {
         var type = this.getAttribute('data-value');
         if (type == 'False')
            return false;
         window.location = this.id;
         return false;
      });

    });
    function test() {
      console.log('FSDFASF')
    }

    function onDoubleClick(item) {
      window.location.href = "s";
    }
    function itemOnClick(item) {

      if (current_selected_item == item)
        return
      if (current_selected_item)
        $(current_selected_item).attr('style', function (i, s) {
          _str = s || ''
          _str = _str.replace("border-color: #7FCBD8 !important;background: rgba(144, 144, 144, 0.3);", "")
          return _str
        })
      current_selected_item = item
      $(current_selected_item).attr('style', function (i, s) { return (s || '') + 'border-color: #7FCBD8 !important;background: rgba(144, 144, 144, 0.3);' })
      console.log(item)
    }