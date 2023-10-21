function close_edit_profile_block(){
    document.querySelector('.profile-header-wrapper').style.display = 'block'
    document.querySelector('.edit-profile-header-block').style.display = 'none'

    return
}

function refresh_user_profile(form_json){

    let form_fields = JSON.parse(form_json)
    const mon = form_fields.moniker
    const web = form_fields.website
    const cap = form_fields.caption

    document.querySelector('.profile-moniker').innerHTML = mon
    document.querySelector('.profile-website').innerHTML = web
    document.querySelector('.profile-caption').innerHTML = cap


    return
}


function submit_edit_profile_form(){

    // Handle form submission
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

        // Create a FormData JSON object to store the fields
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
                close_edit_profile_block()

            }else{
                console.log('Error Updating Profile '+result.status)
            }
        })
        .catch((error) => {
            error = "Error updating profile => "+error
            console.log('Update Error ' + result.status+ ' ' + errir)
        })

        refresh_user_profile(form_json)
        return false // prevent form from calling an action such as sending the form to another page
    }
}



function open_edit_profile(){
    console.log(' ##### open_edit_profile #####')

    // Hide Profile Header and Show Edit Block
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
        document.querySelector('#edit-profile-moniker').value = profile_data['moniker']
        document.querySelector('#edit-profile-website').value = profile_data['website']
        document.querySelector('#edit-profile-caption').value = profile_data['caption']

        document.querySelector('#background_img').value = profile_data['background_img_url']
        document.querySelector('#avatar').value = profile_data['avatar_url']
    })
    .catch((error) => {
        error = 'edit_profile(): Error Fetching User Profile Data => '+error
        // display_UI_message(error)
      });
    console.log('Data Feteched')
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
        edit_profile_cancel_btn.addEventListener('click', () => cancel_edit_profile());
    }else{
        console.log('Cant find id => #edit-profile-submit')
    }

    return
}

function create_new_post(){
    console.log('Create New Post')
    //alert('create post')
    // get new-post-element
    const new_post_element = document.querySelector('.new-post-wrapper')

    // toggle new_post_element on
    new_post_element.style.display = 'block';

    // Intercept Form Submission for Javascript to Handle it inside the Client
    let new_post_form = document.querySelector('.new-post-form')
    console.log('new post form  => ', new_post_form)
    if (new_post_form != null){
        new_post_form.onsubmit = function() {
 

            console.log('creating JSON')
            // Create JSON String to Send to the API
            const newpost_form_data = new FormData()


            // Extract INPUT Values then add to JSON
            
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

            // Get New Post Form Elements Image_field
            const post_message_input  = document.querySelector('#post-message')
            const post_message_val = post_message_input.value 
            if (post_message_val != null){
                newpost_form_data.append('message', post_message_val) 
            }

            // Get New Post Form Elements Image_field
            const post_image_input = document.querySelector('#post-image')
            const post_image_file = post_image_input.files[0]
            console.log('Javascript: post_image_file', post_image_file)
            if(post_image_file != null){
                newpost_form_data.append('image_file', post_image_file) 
            }

            console.log('calling fetch /create_post path')
            // Call API with Fetch POST to create new Post in the Database
            fetch("/create_post", {
                method: "POST",
                body: newpost_form_data
            })
            .then(response => {
                response_status = response.status
                return response.json()
            })
            .then(result => {
                if (response_status === 201){
                    close_post()
                    //reload profile ??
                    // if user_is_home
                    //    reload profile
                    // else
                    //    do nothing
                }else{
                    // Display UI Error Message
                    console.log('Javascript: Post Fail')
                }
            })
            .catch((error) => {
                error = "create_new_post() BAH ERROR: Error posting => "+error
                console.log(error)
            })

            // Prevent Form from Calling the action ="..." part
            return false


        }
    }else{
        console.log('create_new_post() ERROR: Cant find class => .new-post-form')
    }
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

function cancel_edit_profile(){
    console.log('cancel_edit_profile')
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

function write_emoji(e){
    console.log(e.target)
    emoji = e.target.innerHTML

    // get post message element
    message_body_element = document.querySelector('#post-message')
 
    // get the message body text and add the emoji to the end
    message_body = message_body_element.value
    message_body = message_body + emoji

    // add the selected emoji to the message
    message_body_element.value = message_body

    return
}

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

    .then( result => {
        if(response_status === 201){
            console.log("database updated with upduke for post => ", post_id)
            // Add class.star-icon-active
            star_icon = post_element.querySelector('.star-icon')
            star_icon.classList.add('star-icon-active')

            // Update Count
            updukes = result.total_updukes
            upduke_count = document.querySelector('.upduke-count')
            upduke_count.innerHTML = updukes        
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
    post_btn_element.addEventListener('click', () => create_new_post())

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
    return
}




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

    // Initialise to indicate scrolling is not at the end
    var pages_available_flag = true

    // Add Event Listener to Newsfeed Scroll
    newsfeed_element.addEventListener('scroll', () => {

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

                // Determine the Current Page after Fetch page load
                page_num = parseInt(state_data_div.dataset.pagenum) 
                // Determine requested_page, this is always next page
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

                        // Add html_post_set to the newsfeed_element
                        newsfeed_element.insertAdjacentHTML("beforeend", post_set)

                        // Increment state_data in the DOM for pagenum
                        page_num++
                        document.querySelector('.profile-header-wrapper').dataset.pagenum = page_num

                        // Add Event Listener to the new posts for the upduke star
                        // select new posts class = newpost-{{page_num}}, ie newsfeed-pg3, newsfeed-pg4 etc
                        newsfeed_pg_class = 'newsfeed-pg'+page_num 
                        new_newsfeed_page = document.getElementsByClassName(newsfeed_pg_class)
                        // Add upduke star EventLister to new posts
                        let i = 0
                        for(i = 0; i < new_newsfeed_page.length; i++){
                            star_icon = new_newsfeed_page[i].querySelector('.star-icon')
                            star_icon.addEventListener('click', upduke_post)
                         }

                    }else if(response_status === 200){
                        // the requested page was One more than the Total Number of Pages
                        // Display scroll end message
                        endscroll_html =    `<div class = 'feedpost-wrapper'>
                                                <div>There's nuthin in the sububs, Bub</div>
                                            </div>`
                        newsfeed_element.insertAdjacentHTML("beforeend", endscroll_html)

                        // Set pages_available_flag = false
                        pages_available_flag = false
                        
                    }else if(response_status === 300){
                        error_message = user_posts_wrapper.message
                        error = `<div class = 'feedpost-wrapper'><div>${error_message}</div></div>`
                        newsfeed_element.insertAdjacentHTML("beforeend", error)

                    }else if(response_status === 400){
                        error_message = user_posts_wrapper.message
                        error = `<div class = 'feedpost-wrapper'><div>${error_message}</div></div>`
                        newsfeed_element.insertAdjacentHTML("beforeend", error)

                    }else if(response_status === 500){
                        error_message = user_posts_wrapper.message
                        error = `<div class = 'feedpost-wrapper'><div>${error_message}</div></div>`
                        newsfeed_element.insertAdjacentHTML("beforeend", error)
                    }
                })
                .catch(error => {
                    error = "Error fetching new post set: " + error
                    error_html = `<div class = 'feedpost-wrapper'><div>${error}</div></div>`
                    newsfeed_element.insertAdjacentHTML("beforeend", error_html)
                })// END Fetch
            }// END if (scroll_end_point == true)
        }// END If page_num != 'TheEnd'
    })

    // Exit Watch Scroller
    return
}

function load_postfeed(){
    
}


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



document.addEventListener('DOMContentLoaded', function() {

    console.log("javascript loaded")

 

    // SHow the Appropriate Buttons on the Profile
    initialise_profile_buttons()
    watch_newsfeed_scrolling()
    load_postfeed()

    // Use buttons to toggle between views


  

  
  });





