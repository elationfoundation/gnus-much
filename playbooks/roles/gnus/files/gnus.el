(require 'notmuch)
(add-hook 'gnus-group-mode-hook 'lld-notmuch-shortcut)
(require 'org-gnus)

(defun lld-notmuch-shortcut ()
  (define-key gnus-group-mode-map "GG" 'notmuch-search)
  )

(defun lld-notmuch-file-to-group (file)
  "Calculate the Gnus group name from the given file name.
    "
  (let ((group (file-name-directory (directory-file-name (file-name-directory file)))))
    (setq group (replace-regexp-in-string ".*/Maildir/" "nnimap+local:" group))
    (setq group (replace-regexp-in-string "/$" "" group))
    (if (string-match ":$" group)
        (concat group "INBOX")
      (replace-regexp-in-string ":\\." ":" group))))

(defun lld-notmuch-goto-message-in-gnus ()
  "Open a summary buffer containing the current notmuch
    article."
  (interactive)
  (let ((group (lld-notmuch-file-to-group (notmuch-show-get-filename)))
        (message-id (replace-regexp-in-string
                     "^id:" "" (notmuch-show-get-message-id))))
    (setq message-id (replace-regexp-in-string "\"" "" message-id))
    (if (and group message-id)
        (progn 
          (switch-to-buffer "*Group*")
          (org-gnus-follow-link group message-id))
      (message "Couldn't get relevant infos for switching to Gnus."))))

(define-key notmuch-show-mode-map (kbd "C-c C-c") 'lld-notmuch-goto-message-in-gnus)

(setq gnus-select-method
      '(nnimap "Mail"
	       (nnimap-address "localhost")
	       (nnimap-stream shell)
	       (nnimap-shell-program "/usr/lib/dovecot/imap -o mail_location=maildir:$HOME/Mail")
	       ))
