resource "null_resource" "local-exec-single" {
  provisioner "local-exec" {
    command = "echo 'Hello World'"
  }
}

# Calling multi-exec requires the file to be formed with the approriate line-endings
# LF for linux and CRLF for windows
resource "null_resource" "local-exec-multi" {
  provisioner "local-exec" {
  command = <<EOT
    echo 'Hello World' ;
    echo 'good-bye world'
  EOT
  }
}
