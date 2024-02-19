 var current_selected_item;
    $(document).ready(function () {

      $('.upload-btn .upload-btn-input').change(function (ev) {
        $('.upload-btn .upload-btn-form').submit()
      });
      $('.dropdown-menu #rename_button').on('click', function (ev){
        var item_hash = $(current_selected_item).attr('data-hash');
        var is_folder = $(current_selected_item).attr('data-value');
        var item_placeholder_url = null;
        if (is_folder === 'True')
           item_placeholder_url = $('#form_name_update').attr('data-folder-url');
        else
           item_placeholder_url = $('#form_name_update').attr('data-file-url');
        var item_rename_url = item_placeholder_url.replace('placeholder', item_hash)
        $('#form_name_update').attr('action', item_rename_url)

      })
      $('.elm ').click(function (ev) {
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