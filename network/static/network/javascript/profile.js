
function get_state_data(){
    // This is just for reference
    // Load State Data

    const profile_user_id = document.querySelector('.profile-header-wrapper').dataset.profileuserid
    const current_user_id = document.querySelector('.profile-header-wrapper').dataset.currentuserid
    const following_status = document.querySelector('.profile-header-wrapper').dataset.followingstatus
    const user_is_home = document.querySelector('.profile-header-wrapper').dataset.user_is_home

    // Get Postfeedname
    const postfeed_name = document.querySelector('.profile-header-wrapper').dataset.postfeed_name

    // Determine what page we are on
    var page_num = parseInt(document.querySelector('.profile-header-wrapper').dataset.pagenum)

    // post_id contained in <div class = 'feedpost-wrapper>
    const post_id_element = document.querySelector('feedpost-wrapper')


    // the feedpost-wrapper contains a dataset-post_id which is the post_id primary-key for each post
    // FInding a post is best done by selecting the dataset and searching for a specific post_id
    let post_id = 100
    var find_post = document.querySelector('div[data-post_id="' + post_id + '"]');

    return
}








/****************************************************************************** */
/*
/*  Functions that Handle Creating, Editing and Closing the User Profile header
/*
/*
/****************************************************************************** */

function open_edit_profile(){
    console.log(' ##### open_edit_profile #####')

    // Show Edit Profile Block
    document.querySelector('.edit-profile-header-block').style.display = 'block'

    // Fetch User Profile Data from Server
    let profile_path = "/get_user_profile"
    console.log('Fetching data from API')
    fetch(profile_path)
    .then(response => {// JSON String Formated Object (Like The envelope)
        // Parse the contents of the response.
        // First  is the status 
        // Then the Json object
        response_status = response.status
        return response.json()
      })
    .then(profile_data => {  // Parsed into usable Javascript Object (like the contents of the envelope)
        // fill edit form with current profile values
        if(response_status == 201){
            document.querySelector('#edit-profile-moniker').value = profile_data['moniker']
            document.querySelector('#edit-profile-website').value = profile_data['website']
            document.querySelector('#edit-profile-caption').value = profile_data['caption']

            //document.querySelector('#background_img').value = profile_data['background_img_url']
            //document.querySelector('#avatar').value = profile_data['avatar_url']

            //console.log("Javascript: image received => ", post_data['avatar_url'])
            //console.log("Javascript: typeof => ", typeof post_data['avatar_url'])
        }else{

        }
    })
    .catch((error) => {
        error = 'edit_profile(): Error Fetching User Profile Data => '+error
        // display_UI_message(error)
      });
    console.log('Data Fetched')
    console.log('Adding Event Listener')

    // Add event listener to the form submit button to call the submit function and the Cancel Button
    // This is not added with the general buttons so that its not available in background when someone visits a profile
    let submit_btn = document.querySelector('#edit-profile-submit')
    if(submit_btn != null){
        submit_btn.addEventListener('click', submit_edit_profile_form)
    }else{
        console.log('Cant find id => #edit-profile-submit')
    }
    // Add event listener to edit-profile-cancel-btn
    let edit_profile_cancel_btn = document.querySelector('#edit-profile-cancel-btn')
    if (edit_profile_cancel_btn != null){
        edit_profile_cancel_btn.addEventListener('click', () => close_edit_profile());
    }else{
        console.log('Cant find id => #edit-profile-submit')
    }

    return
}


function submit_edit_profile_form(){
    // Handle form submission
    // Updates the Database with new Profile Data and then inserts it into DOM
    document.querySelector('.edit-profile-form').onsubmit = function() {
        
        // Capture regulat form inputs
        const moniker_value = document.querySelector('#edit-profile-moniker').value
        const website_value = document.querySelector('#edit-profile-website').value
        const caption_value = document.querySelector('#edit-profile-caption').value

        // Select the background image Input field
        const background_input = document.querySelector('#edit-profile-background-img');
        const background_file = background_input.files[0]; // Get the selected file (the first file if multiple files are allowed).
      
        // Select the avatar image field
        const avatar_input = document.querySelector('#edit-profile-avatar');
        const avatar_file = avatar_input.files[0]; // Get the selected file (the first file if multiple files are allowed).

        // Create a FormData object to store the fields
        // WHen this is sent via the fetch it becomes request.POST and request.FILES
        const form_data = new FormData();

        if (background_file) {
            form_data.append('background_file', background_file);
        }
        if (avatar_file) {
            form_data.append('avatar_file', avatar_file);
        }
        form_data.append('moniker', moniker_value)
        form_data.append('website', website_value)
        form_data.append('caption', caption_value)

        // Fetch POST to API path API Path
        fetch('/update_profile',{
            method: "POST",
            body: form_data
        })
        .then(response => {
            response_status =  response.status
            return response.json()
        })
        .then(result => {      
            if(response_status === 201){
                // Update Successfull

                // Get Html from returned Json
                // This is still to be implemented. 
                // For now browser will show the changes made to the database when 
                //the page is refreshed and reloaded.

                // Close Panel and clear form fields
                close_edit_profile()
            }else{
                console.log('Error Updating Profile '+result.status)
            }
        })
        .catch((error) => {
            error = "Error updating profile => "+error
            console.log('Update Error ' + result.status+ ' ' + error)
        })

        refresh_user_profile(form_data) // Insert New FormData into DOM.
        return false // prevent form from calling an action such as sending the form to another page
    }
}


function close_edit_profile(){
    // CLoses the Edit Profile Panel and resets the contents to Null
    // select the form INPUT elements
    const profile_bg  = document.querySelector('#edit-profile-background-img')
    const profile_av  = document.querySelector('#edit-profile-avatar')
    const profile_mon = document.querySelector('#edit-profile-moniker')
    const profile_web = document.querySelector('#edit-profile-website')
    const profile_cap = document.querySelector('#edit-profile-caption')

    // Reset them to be null
    profile_bg.value = ''
    profile_av.value = ''  
    profile_mon.value = ''
    profile_web.value = ''  
    profile_cap.value = ''

    // Close the Edit Profile Panel
   // Hide Profile Header and Show Edit Block
   document.querySelector('.profile-header-wrapper').style.display = 'block'
   document.querySelector('.edit-profile-header-block').style.display = 'none'

    return
}


function refresh_user_profile(form_data){
    // When this is called the database has been updated with new data.
    // This function inserts the new CharField form data into the Browser User Profile Section
    // IMages require processing on the server so this a halfway solution to updating the Browser content dynamically with Javascript
    // Handling FormData 
    // https://stackoverflow.com/questions/41431322/how-to-convert-formdata-html5-object-to-json
    // https://developer.mozilla.org/en-US/docs/Web/API/FormData

    const mon = form_data.get('moniker')
    const web = form_data.get('website')
    const cap = form_data.get('caption')

    document.querySelector('.profile-moniker').innerHTML = mon
    document.querySelector('.profile-website').innerHTML = web
    document.querySelector('.profile-caption').innerHTML = cap


    return
}

/**************************************************************************************************** */
/********************************* End User Profile Sections **************************************** */


































/*********************************************************************** */
/*
/*  FUnctions that Handle Making a Post to the App
/*  Create, Edit, Closing and Delete
/*
/*********************************************************************** */
function handle_post(post_action, post_id, post_html_block){ // post_action is either 'edit' or 'create'
    console.log('Javascript: Function Header ### handle_post()')
    //alert('create post')
    // get new-post-element
    const new_post_element = document.querySelector('.new-post-wrapper')

    // toggle new_post_element on
    new_post_element.style.display = 'block';

    // FORM HANDLER
    // Intercept Form Submission for Javascript to Handle it inside the Client
    let new_post_form = document.querySelector('.new-post-form')
    new_post_form.onsubmit = function() {

        console.log('creating FormData')
        // Create FormData to Send to the API
        const newpost_form_data = new FormData()


        // Extract INPUT Values then add to FormData
        
        // Get New Post Form Elements Image_field. 
        // Select the ID's for the fields defined in the form
        // Constructing the FormData Key:Values
        // First Part is the variabel name of the form field ie the Left side of the '=' sign in forms.py
        // Second part is the Value contained in the Input field
        const post_title_input = document.querySelector('#post-title')
        const post_title_val = post_title_input.value
        if(post_title_val){
            newpost_form_data.append('title', post_title_val) 
        }   

        // Get New Post Form Elements Image_field VALUE
        const post_message_input  = document.querySelector('#post-message')
        const post_message_val = post_message_input.value 
        if (post_message_val != null){
            newpost_form_data.append('message', post_message_val) 
            console.log("Javascript: Appending message body to FormData ", post_message_val)
        }

        // Get New Post Form Elements Image_field FILE
        const post_image_input = document.querySelector('#post-image')
        const post_image_file = post_image_input.files[0]
        console.log('Javascript: post_image_file', post_image_file)
        if(post_image_file != null){
            newpost_form_data.append('image_file', post_image_file) 
        }

        console.log('calling fetch /handle_post')
        if (post_action == 'create'){
            // formulate create api path
            api_path = "/handle_post"
            api_method = 'POST'
            console.log("Javascript: New Post => ", api_path, api_method)
        }else{
            // formulate edit api path
            api_path = "/handle_post/edit/"+post_id
            api_method = 'POST'
            console.log("Javascript: Edit Post => ", api_path, api_method)
        }
        // Call API with Fetch POST to create or update new Post in the Database
        fetch(api_path, {
            method: api_method,
            body: newpost_form_data
        })
        .then(response => {
            response_status = response.status
            return response.json()
        })
        .then(result => {
            if (response_status === 201){
                close_post()
                const state_data_div = document.querySelector('.profile-header-wrapper')
                user_is_home = state_data_div.dataset.user_is_home
                // Add New Post to the top of the Postfeed
                if (user_is_home == 'True'){
                    new_post_html = result.html_post_set
                    const newsfeed_element = document.querySelector('#newsfeed')

                    // remove the old post
                    if (post_id != 0){
                        var old_post = document.querySelector('div[data-post_id="' + post_id + '"]');
                        old_post.remove()
                    }
                    // add the new post
                    newsfeed_element.insertAdjacentHTML("afterbegin", new_post_html)

                    // Add Event Listener to the Upduke Button
                    // Add Event Listener to the Edit Button
                    // Add Event Listener to the Delete Button
                    // It will be there when the page is reloaded so not crazy important
                }else{
                    console.log("user is away")
                }
            }else if (response_status = 500){
                console.log("Javascript: Server Save Post Error => ", result.error)
            }else{
                // Display UI Error Message
                console.log('Javascript: Post Fail')
            }
        })
        .catch((error) => {
            error = "handle_post() BAH ERROR: Error posting => "+error
            console.log(error)
        })

        // Prevent Form from Calling the action ="..." part
        return false
    }

    return
}


function open_edit_post(e){
    console.log("javascript: open_edit_post()")

    // Get Post Data for the post that was clicked
    const post_html_block = e.target.parentElement.parentElement.parentElement
    post_id = post_html_block.dataset.post_id
    console.log("Javascrip: post_id => ", post_id)

    let get_post_data = '/get_post_data/'+post_id
    console.log("javascript: about to call fetch => ", get_post_data)
    // Fetch the Data for the post that has been clicked
    fetch(get_post_data, {
        method: 'GET'
    })
    .then(response => {
        response_status = response.status
        return response.json()
    })
    .then(post_data => {
        if(response_status = 201){
            console.log("javascript: Fetch returned status 201")
            // fill edit form with current profile values
            document.querySelector('#post-title').value = post_data['title']
            document.querySelector('#post-message').value = post_data['message']


            // The Image field is a user upload field where the user chooses a file from their device, so you cant prefill it with something thats on the server
            // Instead I will show the current image (if any) in the preview window.


            // Show the image from the database in the image_preview window
            const imagePreview = document.getElementById('image-preview');
            if(imagePreview){
                console.log("Javascipt: imagePreview => ", imagePreview)
            }else{
                console.log("Javascipt: imagePreview => Does not exist")
            }
            if (post_data.image_file_url) {
                console.log("Javascript: post_data.image_file_url exists")
                // Set the src attribute of the <img> element to the image URL
                imagePreview_wrapper = document.querySelector('.image-preview-wrapper')
                imagePreview_wrapper.style.display = "block"
                imagePreview.style.display = "block"
                imagePreview.src = post_data.image_file_url;

                // Make some space in the post panel for the preview
                //post_wrapper =  document.querySelector(".new-post-wrapper")
                //post_wrapper.style.height = '40rem'
            } else {
                console.log("Javascript: post_data.image_file_url Does Not exist")
                // If there is no image, you can hide the <img> element or display a placeholder image
                imagePreview.style.display = 'none'; // Hide the image
                // You can also set a placeholder image like this:
                // imagePreview.src = '/path/to/placeholder.png';
            }
            

            // We now have the all the new form data so we can handle it as though it was a reqular post
            handle_post('edit', post_id, post_html_block)

        }else if (response_status = 404){
            console.log("Javascript: Error status 404 => ", post_data['error'])
        }else if (response_status = 400){
            console.log("Javascript: Error status 400 => ", post_data['error'])
        }
    })
    .catch( error => {
        console.log("javascript: ERROR ", e)
    })

    return
}

function write_emoji(e){
    // Allows a User to insert an emoji into the message
    console.log("Javascript: write_emoji",e.target)

    // get emoji
    emoji = e.target.innerHTML
    console.log("Javascript: write_emoji",e.target)

    // get post message element
    message_body_element = document.querySelector('#post-message')
 
    // get the message body text and add the emoji to the end
    message_body = message_body_element.value
    message_body = message_body + emoji

    // add the selected emoji to the message
    message_body_element.value = message_body
    console.log("Javascript: message_body => ", message_body_element)

    return
}



function close_post(){
    // select the form INPUT elements
    const post_title = document.querySelector('#post-title')
    const post_body = document.querySelector('#post-message')
    const post_image = document.querySelector('#post-image')

    // Reset text fields to be null
    post_title.value = ''
    post_body.value = ''  


    // Clear File Uploads and Previews
    const image_input = document.querySelector('#post-image')
    const image_preview = document.querySelector('#image-preview')
    const image_filename_block = document.querySelector('#image-upload-name')

    // Clear the preview display and hide
    image_preview.src = '';
    image_preview.style.display = 'none';
    image_preview.parentElement.style.display = 'none';

    // Clear Image Label field
    document.querySelector('#image-upload-name').innerHTML = 'No Uploads'

    // Clear the upload file
    post_image.files[0]=''
    post_image.value = ''

    // Close the New Post Panel
    const post_element = document.querySelector('.new-post-wrapper')
    post_element.style.display = 'none'

    return
}

/********************************************************************************************************** */
/****************************************** End Handle Post Section *************************************** */
























/*************************************************************************************** */
/*
/* Event Handler setup for watching the postfeed for Pagination and the Infinte Scroller
/*
/*
/*************************************************************************************** */
// Initialise to indicate scrolling is not at the end. 
// This is a Global variable set by the load_postfeed() function to stop the scroller when it reached the absolute end
// Then its set to False when it recieves 200 status from the API
console.log("Watch_newsfeed_scrolling: assigning pages_available_flag = ", pages_available_flag)
var pages_available_flag = true
function watch_newsfeed_scrolling(){
    console.log("################ watch_newsfeed_scrolling() #######################")
    // Note:
    // This function is called on page load, and it adds the event listener to the newsfeed scroll then exit
    // The variables initialised at the top are available as Global variables to the Callback function of the EVentListener.
    // They're initialised once when the function is called whereas the Callback function loops every time the
    // scrollbar is moved 
    // Once the scroll is triggered, the callback function will run continuously until the page is refreshed.
    // On page refresh it will await the scroll event
    // Variables inside the Event Listener Callback that rely on state data from the DOM will have to explicitly 
    // check them when necessary From within the callback.


    // Global variables that persist when the Calback is triggered

    // Select Newsfeed Element
    const newsfeed_element = document.querySelector('#newsfeed')

    // Get state data
    const state_data_div    = document.querySelector('.profile-header-wrapper')
    const profile_user_id   = state_data_div.dataset.profileuserid // User who owns the profile
    const current_user_id   = state_data_div.dataset.currentuserid // Logged-in User 
    const following_status  = state_data_div.dataset.followingstatus // True or False
    const user_is_home      = state_data_div.dataset.user_is_home // True or False

    // Get Postfeedname
    const postfeed_name = state_data_div.dataset.postfeed_name // 'homeposts' | 'awayposts' | 'frenposts'

    // Initialise the page we are on. This should always be 1 when this function is called 
    var page_num = parseInt(state_data_div.dataset.pagenum) 

    // Add Event Listener to Newsfeed Scroll
    newsfeed_element.addEventListener('scroll', () => {
        console.log("Watch_newsfeed_scrolling: Checking if pages_available_flag = ", pages_available_flag)
        if (pages_available_flag == true){
            // Knowing when the Scroll Has reached the Bottom
            // https://stackoverflow.com/questions/3898130/check-if-a-user-has-scrolled-to-the-bottom-not-just-the-window-but-any-element
            //
            // scrollHeight:    newsfeed_height = the combined height of all the posts in the newsfeed_element
            // scrollTop:       newsfeed_top = The position of the top of the scroll
            // clientHeight:    client_height = The visible window ie the height of the newsfeed div
            //
            // The Bottom is reached when the ScrollTop + ClientHeight == ScrollHeight

            // Determine If Scrollbar is at the bottom
            scroll_end_point = Math.abs(newsfeed_element.scrollHeight - newsfeed_element.scrollTop - newsfeed_element.clientHeight) < 1

            if (scroll_end_point == true){
                load_postfeed()

            }// END if (scroll_end_point == true)
        }// END If page_num != 'TheEnd'
        
    })

    // Exit Watch Scroller
    return
}











/************************************************************************************** */
/*
/* Handle Pagination and loading the next page of Users Chosen postfeed
/*
/*
/************************************************************************************** */
function load_postfeed(){
    console.log("################ load_postfeed() #######################")
    // This function will load the next 10 posts in the newsfeed

    // Global variables that persist when the Calback is triggered

    // Select Newsfeed Element
    const newsfeed_element = document.querySelector('#newsfeed')

    // Load state data
    const state_data_div    = document.querySelector('.profile-header-wrapper')
    const profile_user_id   = state_data_div.dataset.profileuserid // User who owns the profile

    // Get Postfeedname
    const postfeed_name = state_data_div.dataset.postfeed_name // 'homeposts' | 'awayposts' | 'frenposts'

    // Initialise the page we are on. This should always be 1 when this function is called 
    var page_num = parseInt(state_data_div.dataset.pagenum) 

    // Determine current page being displayed. 0 means no page which is the initial state
    page_num = parseInt(state_data_div.dataset.pagenum) 

    // Determine requested_page, ie next to load
    requested_page = page_num +1

    // Formulate API Path
    page_path = "/get_newsfeed_page/" + profile_user_id + "/" + postfeed_name + "/" + requested_page
    
    // AJAX Fetch Next Page
    fetch(page_path, {
        "method": "GET"
    })
    .then(response => {
        // Parse API JsonResponse
        response_status = response.status
        return response.json()
    })
    .then(user_posts_wrapper => {                                   
        if(response_status === 201){
            console.log("response_status = ",response_status)
            // returned Json contains two Key:value pairs
            // The first is 'html_post_set': rendered html posts. A block of html code containing all the posts that were requested
            // The second is 'message': An information message

            // Get the contents of the Json that was returned
            post_set = user_posts_wrapper.html_post_set

            // iterate through html_post_set and add to the newsfeed_element
            let i = 0
            for(i=0; i < post_set.length; i++){
                newsfeed_element.insertAdjacentHTML("beforeend", post_set[i])
            }
            // Increment state_data in the DOM for pagenum
            page_num++
            document.querySelector('.profile-header-wrapper').dataset.pagenum = page_num

            // Add Event Listener to the new posts for the upduke star
            // select new posts class = newpost-{{page_num}}, ie newsfeed-pg3, newsfeed-pg4 etc
            newsfeed_pg_class = 'newsfeed-pg'+page_num 
            new_newsfeed_page = document.getElementsByClassName(newsfeed_pg_class)
            // Add upduke star EventLister to new posts
            for(i = 0; i < new_newsfeed_page.length; i++){
                star_icon = new_newsfeed_page[i].querySelector('.star-icon')
                star_icon.addEventListener('click', upduke_post)
                }

            // Add open_edit_post EventListener to new posts
            for(i = 0; i < new_newsfeed_page.length; i++){
                edit_icon = new_newsfeed_page[i].querySelector('.edit-post-icon')
                if(edit_icon != null){
                    edit_icon.addEventListener('click', open_edit_post)
                }
            }


            pages_available_flag = true
            console.log("load_postfeed. Returning pages_available_flag = ", pages_available_flag)           

        }else if(response_status === 200){
            // the requested page was One more than the Total Number of Pages
            // Display scroll end message
            endscroll_html =    `<div class = 'feedpost-wrapper'>
                                    <div>There's nuthin in the sububs, Bub</div>
                                </div>`
            newsfeed_element.insertAdjacentHTML("beforeend", endscroll_html)

            // Set pages_available_flag = false
            pages_available_flag = false
            console.log("load_postfeed. Returning pages_available_flag = ", pages_available_flag)
            
        }else if(response_status === 300){
            error_message = user_posts_wrapper.message
            error = `<div class = 'feedpost-wrapper'><div>${error_message}</div></div>`
            newsfeed_element.insertAdjacentHTML("beforeend", error)
            pages_available_flag = false         

        }else if(response_status === 400){
            error_message = user_posts_wrapper.message
            error = `<div class = 'feedpost-wrapper'><div>${error_message}</div></div>`
            newsfeed_element.insertAdjacentHTML("beforeend", error)
            pages_available_flag = false             

        }else if(response_status === 500){
            error_message = user_posts_wrapper.message
            error = `<div class = 'feedpost-wrapper'><div>${error_message}</div></div>`
            newsfeed_element.insertAdjacentHTML("beforeend", error)
            pages_available_flag = false           
        }
    })
    .catch(error => {
        error = "Error fetching new post set: " + error
        error_html = `<div class = 'feedpost-wrapper'><div>${error}</div></div>`
        newsfeed_element.insertAdjacentHTML("beforeend", error_html)
        pages_available_flag = false      
    })// END Fetch

    return 
}



/************************************************************************************** */
/*
/* Event Handler setup for watching the postfeed for Pagination & the Infinte Scroller
/*
/*
/************************************************************************************** */
// Initialise to indicate scrolling is not at the end. 
// This is a Global variable set by the load_postfeed() function to stop the scroller when it reached the absolute end
// When this happens, its set to False. This is triggered when load_postfeed() recieves 200 status from the API
var pages_available_flag = true

// Notes:
// This function is called on page load, and it adds the event listener to the newsfeed scroll then exit and wait for event
// The variables initialised at the top are available as Global variables to the Callback function of the EVentListener.
// They're initialised once when the function is called whereas the Callback function loops every time the
// scrollbar is moved 
// Once the scroll is triggered, the callback function will run continuously until the page is refreshed.
// On page refresh it re-initialises and once again waits the scroll event
// Variables inside the Event Listener Callback that rely on state data from the DOM will have to explicitly 
// check them when necessary From within the callback.


// Global variables inside the function persist when the Calback is triggered


function watch_newsfeed_scrolling(){
    // Select Newsfeed Element
    const newsfeed_element = document.querySelector('#newsfeed')

    // Add Event Listener to Newsfeed Scroll
    newsfeed_element.addEventListener('scroll', () => {
        console.log("Watch_newsfeed_scrolling: Checking if pages_available_flag = ", pages_available_flag)
        // Knowing when the Scroll Has reached the Bottom
        // https://stackoverflow.com/questions/3898130/check-if-a-user-has-scrolled-to-the-bottom-not-just-the-window-but-any-element
        //
        // scrollHeight:    newsfeed_height = the combined height of all the posts in the newsfeed_element
        // scrollTop:       newsfeed_top = The position of the top of the scroll
        // clientHeight:    client_height = The visible window ie the height of the newsfeed div
        //
        // The Bottom is reached when the ScrollTop + ClientHeight == ScrollHeight
        if (pages_available_flag == true){
            // Determine If Scrollbar is at the bottom
            scroll_end_point = Math.abs(newsfeed_element.scrollHeight - newsfeed_element.scrollTop - newsfeed_element.clientHeight) < 1

            if (scroll_end_point == true){
                load_postfeed()
            }
        }
    })

    // Exit Watch Scroller
    return
}


/******************************************************************************************************************** */
/*************************************** End Pagination and Infinite Scroller *************************************** */





























/*********************************************************************** */
/*
/*  Functions that Handle Giving a Post an Upduke
/*
/*  called when eventListener on star-icon is clicked. class = 'star-icon'
/*
/*********************************************************************** */
function upduke_post(e){
    console.log("#### upduke_post ####")
    // Note: this function uses the event (e) variable
    // This mean it must be called using the name 'upduke_post' to get the event that called it 'e'
    // not '() => upduke_post()' , This wont supply the event trigger 'e'
    const post_element = e.target.parentElement.parentElement.parentElement
    console.log('Clicked => ', post_element)
    const post_id =  parseInt(post_element.dataset.post_id)


    // formulate path to the API upduke function
    const upduke_path = '/upduke_post/'+post_id
    // Fetch PUT the Upvote to the API

    fetch(upduke_path, {
        method: 'PUT',
    })
    .then(response => {
        response_status = response.status
        return response.json()
    })

    .then(post_engagement => {
        if(response_status === 201){
            console.log("database updated with upduke for post => ", post_id)
            // Toggle class.star-icon-active
            console.log("post_element => ", post_element)
            star_icon = post_element.querySelector('.star-icon')
            star_icon.classList.toggle('star-icon-active')

            // Update Count
            upduke_counter = post_engagement.total_updukes
            console.log("upduke count => ", upduke_counter)
            upduke_count_div = post_element.querySelector('.upduke-count')
            console.log("upduke count div => ", upduke_count_div)
            upduke_count_div.innerHTML = upduke_counter        
        }
    })
    .catch(error => {
        error = "Error Engagement_m2m: " + error
        error_html = `<div class = 'feedpost-wrapper'><div>${error}</div></div>`
        const newsfeed_element = document.querySelector('#newsfeed')
        newsfeed_element.insertAdjacentHTML("beforeend", error_html)
    })// END Fetch
    return
}
/******************************************************************************************************** */
/******************************************* End Upduke Section ***************************************** */





























/*********************************************************************** */
/*
/* Functions for Handling the Follow Unfollow functionality
/*
/*
/*********************************************************************** */

function show_follow_or_unfollow_btn(btn_choice){
    follow_btn_element = document.querySelector('#follow-btn')
    console.log("follow btn => ", follow_btn_element)
    unfollow_btn_element = document.querySelector('#unfollow-btn')
    console.log("unfollow btn => ", unfollow_btn_element)
    if (btn_choice == 'follow'){
        // Follow Button is Displayed after a user has been unfollowed so Hide Unfollow Buttin
        follow_btn_element.style.display = 'block'
        unfollow_btn_element.style.display = 'none'

    }else{
        // UnFollow Button is Displayed after a user has been followed so Hide Follow Buttin
        follow_btn_element.style.display = 'none'
        unfollow_btn_element.style.display = 'block'

    }
    return
}

function decrement_followers(){
    follower_count_element =  document.querySelector('.follower-count')
    num_followers = parseInt(follower_count_element.innerHTML)
    num_followers = num_followers - 1
    console.log('num followers = ', num_followers)
    follower_count_element.innerHTML = num_followers
    
    return
}

function increment_followers(btn_choice){
    follower_count_element =  document.querySelector('.follower-count')
    num_followers = parseInt(follower_count_element.innerHTML)
    num_followers = num_followers + 1
    console.log('num followers = ', num_followers)
    follower_count_element.innerHTML = num_followers
    
    return
}

function follow(){
    console.log('follow clicked')
    // Follow User by calling Fetch Follow
    let profile_user_id = document.querySelector('.profile-header-wrapper').dataset.profileuserid
    profile_user_id = parseInt(profile_user_id)
    
    let current_user_id = document.querySelector('.profile-header-wrapper').dataset.currentuserid
    current_user_id = parseInt(current_user_id)
    
    const following_status = document.querySelector('.profile-header-wrapper').dataset.followingstatus

    if (profile_user_id != current_user_id){ // Ensure a User cant Follow themselves
        fetch(`/follow/${profile_user_id}`)
        .then(response => {
            // Parse the contents of the response.
            // First  is the status 
            // Then the Json object
            response_status = response.status
            return response.json()
          })
        .then(result => {
            if (response_status === 201){
                user_message = 'Successfully followed this User. result.status='+result.status
                show_follow_or_unfollow_btn('unfollow')
                increment_followers()
            }else{
                user_message = 'Cant follow this User. result.status='+result.status
            }
        })
        .catch( error => {
            error_message = "ERROR : " + error
            console.log(error)
        })
    }   
}

function unfollow(){
    console.log('unfollow clicked')
    // unFollow User by calling Fetch unFollow
    let profile_user_id = document.querySelector('.profile-header-wrapper').dataset.profileuserid
    profile_user_id = parseInt(profile_user_id)
    
    let current_user_id = document.querySelector('.profile-header-wrapper').dataset.currentuserid
    current_user_id = parseInt(current_user_id)

    const following_status = document.querySelector('.profile-header-wrapper').dataset.followingstatus

    if (profile_user_id != current_user_id){
        fetch(`/unfollow/${profile_user_id}`)
        .then(response => {
            // Parse the contents of the response.
            // First  is the status 
            // Then the Json object
            response_status = response.status
            return response.json()
          })
        .then(result => {
            if (response_status === 201){
                user_message = 'Successfully unfollowed this User. result.status='+result.status
                // rejig follow unfollow btns
                show_follow_or_unfollow_btn('follow')
                decrement_followers()
            }else{
                user_message = 'Cant unfollow this User. result.status='+result.status
                console.log(user_message, result.status)
            }
        })
        .catch( error => {
            error_message = "ERROR : " + error
            console.log(error)
        })
    }

    return
}

/******************************************************************************************** */
/*********************************** End Follow Unfollow ***********************************  */

























/*********************************************************************** */
/*
/* Initialising all the Button Event Handlers on Page Load
/*
/*
/*********************************************************************** */
function initialise_profile_buttons(){
    // retrieve profile dataset information
    console.log('initialise_profile_buttons')

    // Get state data
    const profile_user_id = document.querySelector('.profile-header-wrapper').dataset.profileuserid
    const current_user_id = document.querySelector('.profile-header-wrapper').dataset.currentuserid
    const following_status = document.querySelector('.profile-header-wrapper').dataset.followingstatus
    const user_is_home = document.querySelector('.profile-header-wrapper').dataset.user_is_home

    // Get Postfeedname
    const postfeed_name = document.querySelector('.profile-header-wrapper').dataset.postfeed_name

    // Determine what page we are on
    var page_num = parseInt(document.querySelector('.profile-header-wrapper').dataset.pagenum)

    // Add event listeners to edit profile button
    let edit_profile_btn = document.querySelector('#edit-profile-btn')
    if (edit_profile_btn != null){
        edit_profile_btn.addEventListener('click', () => open_edit_profile());
    }

      // Add event listeners to Show All Posts Button
      let all_posts_btn = document.querySelector('#all-posts-btn')
      if (all_posts_btn != null){
          all_posts_btn.addEventListener('click', () => show_all_posts());
      }  



    // Add event listeners to follow and unfollow button
    let follow_btn = document.querySelector('#follow-btn')
    if (follow_btn != null){
        console.log("adding follow button")
        follow_btn.addEventListener('click', () => follow());
    }
    let unfollow_btn = document.querySelector('#unfollow-btn')
    if (unfollow_btn != null){
        console.log("adding unfollow button")
        unfollow_btn.addEventListener('click', () => unfollow());
    }

    // Add event listeners to nav Post button
    const post_btn_element = document.querySelector('#post-btn')
    post_btn_element.addEventListener('click', () => handle_post('create',0))

    // The New Post form submit button has its own submit action so no eventListener

    // Add event listeners to Post Form Cancel button
    const post_cancel_btn_element = document.querySelector('#new-post-cancel-btn')
    console.log('cancel btn => ', post_cancel_btn_element)
    post_cancel_btn_element.addEventListener('click', () => close_post())

    // Add Image Preview Event Listener on Image Upload INPUT
    const image_input = document.querySelector('#post-image')
    const image_preview = document.querySelector('#image-preview')
    const image_filename_block = document.querySelector('#image-upload-name')

    image_input.addEventListener('change', function () {
        const uploadfile = image_input.files[0]
        const upload_filename = uploadfile.name
        if (uploadfile) {
            const reader = new FileReader()

            reader.onload = function (e) {
                image_preview.src = e.target.result
                image_preview.style.display = 'block'
                image_preview.parentElement.style.display = 'flex'
                image_filename_block.innerHTML = upload_filename
            };

            reader.readAsDataURL(uploadfile);
        } else {
            // Clear the preview if no file is selected
            image_preview.src = '';
            image_preview.style.display = 'none';
            image_preview.parentElement.style.display = 'none';
        }
    });


    // Add eventListsner to emojis
    let emojis_list = document.getElementsByClassName('emoji')
    console.log('emoji_list.length = ', emojis_list.length)
    for(let i = 0; i < emojis_list.length; i++){

        emojis_list[i].addEventListener('click', write_emoji)
    }

    // Add EventListener to the Media Upload Icons
    // This event listener autoclicks the Choose File Button associated with teh INPUT Field (which has been hidden)
    image_upload = document.querySelector('#image-media')
    image_upload.addEventListener('click', () => {
        default_choose_file = document.querySelector('#post-image')
        default_choose_file.click()
    })
    // If current_user is not following the profile display follow else unfollow
    if (user_is_home === 'False'){
        if (following_status == 'False'){
            show_follow_or_unfollow_btn('follow')
        }else{
            show_follow_or_unfollow_btn('unfollow')
        }
    }// else user is on their home profile and there are no follow/unfollow buttons


    // Add Event Listeners to the Star Buttons
    star_upvote_btns = document.getElementsByClassName('star-icon')
    for (let i=0; i < star_upvote_btns.length; i++){
        star_upvote_btns[i].addEventListener('click', upduke_post)
    }

    // Add Event Listeners to the Pagination buttons
    // Having both pagination buttons and an infinite scroller will require integrating them both 
    // It makes sense to have one or the other and Im going for the infiinte scroller
    // and leaving the next previous buttons for now.
    return
}

/********************************************************************************************** */
/********************** End Initialise Butoons and Event Handlers ***************************** */





/*********************************************************************** */
/*
/* Main Javascript Function on DOM Content Loaded
/*
/*
/*********************************************************************** */
document.addEventListener('DOMContentLoaded', function() {
    // SHow and addEventListsners to the Appropriate Buttons on the Profile
    initialise_profile_buttons()

    // Initialise Infinte Scroller
    watch_newsfeed_scrolling()

    // load first page of Current Users Home postfeed
    load_postfeed()

  });












  /*

function preview_image_upload(image_input){
    const file = input.files[0];
    if (file) {
        const reader = new FileReader();

        reader.onload = function (e) {
            preview.src = e.target.result;
            preview.style.display = 'block';
        };

        reader.readAsDataURL(file);
    } else {
        // Clear the preview if no file is selected
        preview.src = '';
        preview.style.display = 'none';
    }
}




function get_cursor_element(){
    // trach where the cursor is
    document.addEventListener("mousemove", function(event) {
        // Get the cursor's X and Y coordinates
        var x = event.clientX;
        var y = event.clientY;
    
        // Get the DOM element at the cursor's position
        var elementAtCursor = document.elementFromPoint(x, y);
    
        // Now, 'elementAtCursor' contains the DOM element at the cursor's position
        console.log(elementAtCursor);
    });
}




function old_close_edit_profile_block(){
    document.querySelector('.profile-header-wrapper').style.display = 'block'
    document.querySelector('.edit-profile-header-block').style.display = 'none'

    return
}
*/



