# Dropzone Action Info
# Name: hpShare
# Description: Share file via hpShare.
# Handles: Files
# Events: Clicked, Dragged
# Creator: BlahGeek
# URL: https://github.com/blahgeek/hpShare
# OptionsNIB: ExtendedLogin
# KeyModifiers: Option
# Version: 2.0
# RunsSandboxed: Yes
# MinDropzoneVersion: 3.0

require 'rubygems'
 
def handle_errors(line)
  if line[0..4] == "curl:"
    if line[6..-1] =~ /Couldn't resolve/
      $dz.fail("Please check your network connection")
    elsif line[6..-1] =~ /403 FORBIDDEN/
      $dz.fail("Invalid username or password")
    else
      $dz.fail(line[6..-1])
    end
  end
end


def curl_it(cmd, progress=true)

  begin
    require 'json'
  rescue LoadError
    $dz.fail("Gem json not installed")
    Process.exit
  end

  command = "/usr/bin/curl '-#' -f " # it's a hack
  command << cmd
  command << " 2>&1 | tr -u \"\r\" \"\n\""

  last_output = 0
  is_receiving_json = false
  json_output = ""

  IO.popen(command) do |f|
    while line = f.gets
      if line =~ /\{/ or is_receiving_json
        is_receiving_json = true
        json_output << line
      elsif line =~ /%/
        line_split = line.split(" ")
        file_percent_raw = line_split[1]
        if file_percent_raw != nil
          file_percent = file_percent_raw.to_i
          if last_output != file_percent
            $dz.percent(file_percent) if progress == true
            # $dz.determinate(false) if file_percent == 100
          end
          last_output = file_percent
        end
      else
        handle_errors(line)
      end
    end
  end

  return JSON.parse(json_output)

end

def upload_one(filepath, private_)
  $dz.determinate(false)
  filename = File.basename(filepath)
  filepath = filepath.gsub('"', '\"')
  $dz.begin("Uploading #{filename}...")

  permit = curl_it("-u #{ENV['username']}:#{ENV['password']}"\
                   " -F \"filename=#{filename}\" -F private=#{private_}"\
                   " http://#{ENV['server']}/permit/", false)
  $dz.determinate(true)
  ret = curl_it("-F token=#{permit['token']} -F \"file=@#{filepath}\""\
                " http://up.qiniu.com")
  $dz.determinate(false)
  return ret
end

def dragged
  private_ = false
  if ENV["KEY_MODIFIERS"] == "Option"
    private_ = true
  end
  results = $items.map do |item|
    upload_one(item, private_)
  end

  if results.length == 1
    $dz.finish("Done, ID=#{results[0]['id']}, URL Copied.")
    $dz.url(ret["url"])
  else
    ids = results.map{|x| x['id']}.join(',')
    ret = curl_it("-u #{ENV['username']}:#{ENV['password']}"\
                  " -F ids=#{ids} -F private=#{private_}"\
                  " http://#{ENV['server']}/newgroup/", false)
    $dz.finish("Done, #{ret['count']} files uploaded, URL Copied.")
    $dz.url(ret["url"])
  end
end


def clicked
  `open http://#{ENV['server']}/`
end
